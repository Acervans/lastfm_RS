from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.urls import reverse
from django.core.paginator import Paginator

from .forms import *
from bs4 import BeautifulSoup
from backend.src.nrc_vad_analysis import FIELDNAMES, FIELDNAMES_LANG, analyze_string, analyze_text
from backend.src.constants import GENIUS, PYLAST
from backend.src.get_lastfm_data import get_user_data
from backend.research.db_utils import *
from backend.research.recbole_research.recbole_run import load_data_and_model
from urllib.parse import quote

import requests
import pylast
import torch

# Create your views here.

RECSYS_DATA = 'backend/data/recsys_data'
SAVED_PATH = 'backend/research/recbole_research/saved'

RECSYS_DATASET = None

# [PATH, MODEL]
RECSYS_MODELS = {
    'random':  [f'{SAVED_PATH}/RandomRecommender.pth', None],
    'cosine':  [f'{SAVED_PATH}/CosineSimilarityRecommender.pth', None],
    'pop':     [f'{SAVED_PATH}/Pop.pth', None],
    'itemknn': [f'{SAVED_PATH}/ItemKNNRecommender.pth', None]
}

# GLOBAL STORAGE
recs_context = dict()
user_data = dict()
inters = None


def index(request):
    """View function for home page of site."""

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    tables_count = get_tables_count()
    tables_count['useralltracks'] = tables_count['usertoptracks'] + \
        tables_count['userrecenttracks'] + tables_count['userlovedtracks']

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={
            'num_visits': num_visits,
            'stats': tables_count,
        },
    )


def register(request):
    """View function for registration form."""

    if request.method == 'POST':
        # Registration form instance
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user:
                return render(request, 'registration/registration_complete.html')

    else:
        form = RegisterForm()
    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'registration/registration_form.html',
        context={'form': form},
    )


def lastfm_preview(request):

    if request.method == 'GET' and 'artist' in request.GET:
        form = PreviewTrackForm(request.GET)
        if form.is_valid():
            artist = form.cleaned_data.get('artist')
            title = form.cleaned_data.get('title')
            do_lyrics = form.cleaned_data.get('lyrics')

            return render(
                request,
                'lastfm_preview.html',
                get_track_context(artist, title, do_lyrics),
            )

    form = PreviewTrackForm()
    return render(request, 'lastfm_preview_form.html', context={'form': form})


def get_track_context(artist, title, do_lyrics):
    """
    Gets the information from a track required for the lastFM Previewer.
    :param artist: string with artist of the track
    :param title: string with title of the track
    :param do_lyrics: determines whether the lyrics should be searched using the Genius API
    :return context: dict with context of the track
    """
    track = pylast.Track(artist, title, PYLAST)

    yt_id = sp_id = mbid = track_url = artist_url = lyrics = None
    found = False
    try:
        mbid = track.get_mbid()
    except pylast.WSError:
        track = None

    if track:
        found = True
        title = track.get_correction()
        track_url = track.get_url()
        artist = track.get_artist().get_correction()
        artist_url = 'https://www.last.fm/music/' + artist.replace(' ', '+')

        soup = BeautifulSoup(requests.get(
            track_url).content, "lxml")
        plinks = soup.find('ul', {'class': 'play-this-track-playlinks'})

        # get playlinks for youtube and spotify embeds
        if plinks:
            yt_tag = plinks.find(
                'a', {'class': 'play-this-track-playlink--youtube'})
            if yt_tag:
                yt_id = yt_tag.get('data-youtube-id')

            sp_tag = plinks.find(
                'a', {'class': 'play-this-track-playlink--spotify'})
            if sp_tag:
                sp_id = sp_tag.get('href').rsplit('track/')[1]

        # get lyrics from Genius API
        if do_lyrics:
            gsong = GENIUS.search_song(title, artist, get_full_info=False)
            if gsong:
                lyrics = gsong.lyrics

    context = {
        'found': found,
        'title': title,
        'track_url': track_url,
        'artist': artist,
        'artist_url': artist_url,
        'id': mbid,
        'yt_id': yt_id,
        'sp_id': sp_id,
        'do_lyrics': do_lyrics,
        'lyrics': lyrics,
    }
    return context


def vad_analysis(request):
    if request.method == 'POST':
        form = VADAnalysisForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            mode = form.cleaned_data.get('mode')
            method = form.cleaned_data.get('method')
            lang_check = form.cleaned_data.get('lang_check')

            if lang_check:
                fieldnames = FIELDNAMES_LANG
            else:
                fieldnames = FIELDNAMES

            if method == 'text':
                fun = analyze_string
                fieldnames = fieldnames[1:]
                fieldnames[0] = 'Text'
            else:
                fun = analyze_text

            return render(
                request,
                'vad_analysis.html',
                {'fieldnames': fieldnames,
                 'results': fun(text, mode, True, lang_check),
                 'method': method},
            )
    else:
        form = VADAnalysisForm()

    return render(request, 'vad_analysis_form.html', context={'form': form})


def user_scraper(request):
    global user_data

    user_data[request.session._get_or_create_session_key()] = dict()

    form = UserScraperForm()
    if request.method == 'GET' and 'username' in request.GET:
        form = UserScraperForm(request.GET)
        if form.is_valid():
            items = ['tracks', 'artists', 'albums', 'tags']
            username = form.cleaned_data.get('username')
            use_db = form.cleaned_data.get('use_database')
            do_items = [form.cleaned_data.get(f'include_{i}') for i in items]

            if not any(do_items[:-1]):
                form.add_error(None, 'Select at least one (non-tag) option')
            else:
                scrape = [[item, form.cleaned_data.get(
                    f'{item}_limit') or 'null'] for i, item in enumerate(items) if do_items[i]]
                return render(
                    request,
                    'user_scraper.html',
                    {
                        'scrape':   scrape,
                        'do_tags':  str(do_items[-1]).lower(),
                        'use_db':   use_db,
                        'username': username,
                        'user_url': PYLAST.get_user(username).get_url()
                    },
                )
    return render(request, 'user_scraper_form.html', context={'form': form})


def scrape_items(request, keys, include):
    global user_data

    session_key = request.session._get_or_create_session_key()

    if request.method == 'GET':
        username = request.GET.get('user')
        limit = request.GET.get('limit')
        use_db = request.GET.get('use_db') == 'True'

        args = {
            'use_items': user_data[session_key],
            f'include_{include}': True,
            f'{include}_limit': int(limit) if limit != 'null' else None
        }
        if use_db:
            user_data[session_key] = data = get_db_user_data(username, **args)
        else:
            user_data[session_key] = data = get_user_data(username, **args)

        if 'ERROR' not in user_data[session_key]:
            data = {k.lower(): user_data[session_key][k.upper()] for k in keys}
        return JsonResponse(data)


def scrape_tracks(request):
    return scrape_items(
        request,
        keys=['recent_tracks', 'loved_tracks', 'top_tracks'],
        include='tracks'
    )


def scrape_artists(request):
    return scrape_items(
        request,
        keys=['top_artists'],
        include='artists'
    )


def scrape_albums(request):
    return scrape_items(
        request,
        keys=['top_albums'],
        include='albums'
    )


def scrape_tags(request):
    return scrape_items(
        request,
        keys=['tags_count', 'item_tags'],
        include='tags'
    )


def recommendations(request):
    global recs_context

    rec_form = RecommendationsForm()
    session_key = request.session._get_or_create_session_key()

    page = request.GET.get('page')

    if page and session_key in recs_context:
        page = page.replace(',', '')
        context = recs_context[session_key]
        new_page = context['page_obj'] = context['paginator'].page(page)
        context['page_range'] = context['paginator'].get_elided_page_range(
            page)
        context['recommendations'] = get_recommendations_context(
            new_page.object_list, new_page.start_index())

        return render(request, 'lastfm_recommend.html', context=context)

    if request.method == 'GET' and 'model' in request.GET:
        recs = None
        rec_form = RecommendationsForm(request.GET)
        if rec_form.is_valid():
            recsys = rec_form.cleaned_data.get('model')
            username = url_user = rec_form.cleaned_data.get('username')
            cutoff = rec_form.cleaned_data.get('cutoff')
            limit = rec_form.cleaned_data.get('limit')
            non_personalized = recsys in ('random', 'pop', 'search')
            predict_args = dict()
            scraper_url = None

            if any(request.GET[field] for field in ('username', 'cosine-tags')) or non_personalized:

                match recsys:
                    case 'random':
                        recsys_form = RandomRecommenderForm(
                            request.GET, prefix='random')
                        if recsys_form.is_valid():
                            seed = recsys_form.cleaned_data.get('seed')
                            seed = seed if seed is not None else int(
                                np.random.randint(2**32 - 1))
                            predict_args = {'generate_new': True}

                            if not RECSYS_MODELS[recsys][1]:
                                RECSYS_MODELS[recsys][1] = load_model(RECSYS_MODELS[recsys][0], config={
                                    'seed': seed,
                                })
                            else:
                                set_seed(seed)

                    case 'cosine':
                        recsys_form = CosineRecommenderForm(
                            request.GET, prefix='cosine')
                        if recsys_form.is_valid():
                            tags = recsys_form.cleaned_data.get('tags')
                            binary = recsys_form.cleaned_data.get('binary')
                            weighted = recsys_form.cleaned_data.get('weighted')
                            topk = recsys_form.cleaned_data.get('topk')

                            RECSYS_MODELS[recsys][1] = load_model(RECSYS_MODELS[recsys][0], config={
                                'weighted_average': weighted,
                                'knn_topk': topk if topk else None,
                                'Vectorizer_Config': {
                                    'binary': binary
                                }
                            })

                            if tags:
                                recs = get_recommendations_by_tags(
                                    tags.split(','), cutoff)

                    case 'search':
                        recsys_form = SearchForm(
                            request.GET, prefix='search')
                        if recsys_form.is_valid():
                            by = ('Track', 'Artist', 'Album')
                            track_query, artist_query, album_query = queries = [
                                recsys_form.cleaned_data.get(f'query_{x.lower()}') for x in by]
                            by_labels = [f"{x} Query \'{q}\'" for i,
                                         x in enumerate(by) if (q := queries[i])]
                            username = ' + '.join(by_labels)

                            tracks = search_tracks(
                                track_query, artist_query, album_query, min(cutoff, 2**63 - 1))
                            recs = list(map(lambda t: (None, t), tracks))

                    case _:
                        if not RECSYS_MODELS[recsys][1]:
                            RECSYS_MODELS[recsys][1] = load_model(
                                RECSYS_MODELS[recsys][0])

                if recs is None:
                    uid, recs = get_recommendations_by_user(
                        username=username,
                        model=RECSYS_MODELS[recsys][1],
                        predict_args=predict_args,
                        cutoff=cutoff
                    )

                    if not uid:
                        if non_personalized:
                            url_user = None
                        else:
                            username = 'Default User'
                            url_user = get_username(1)

                    if url_user:
                        scraper_url = f"{reverse('user_scraper')}?username={quote(url_user)}" \
                            "&use_database=on" \
                            "&include_tracks=on" \
                            "&include_artists=on" \
                            "&include_albums=on" \
                            "&include_tags=on"

                if not limit:
                    limit = cutoff

                p = Paginator(recs, limit)
                first_page = p.page(1)

                recs_context[session_key] = {
                    'username': username or 'Anyone',
                    'scraper_url': scraper_url,
                    'model': dict(rec_form.fields['model'].choices)[recsys],
                    'recommendations': get_recommendations_context(first_page.object_list),
                    'is_paginated': limit and limit < cutoff,
                    'paginator': p,
                    'page_obj': first_page,
                    'page_range': p.get_elided_page_range(1)
                }

                return render(request, 'lastfm_recommend.html', context=recs_context[session_key])
            else:
                rec_form.add_error(
                    'username', 'Fill either username or tags (cosine)')

    random = RandomRecommenderForm(prefix="random")
    cosine = CosineRecommenderForm(prefix="cosine")
    search = SearchForm(prefix="search")
    usernames = get_table_df('user_')['username']
    tags = get_table_df('tag')['name']

    return render(request, 'lastfm_recommend_form.html', context={
        'rec_form': rec_form,
        'random': random,
        'cosine': cosine,
        'search': search,
        'usernames': usernames,
        'tags': tags
    })


def set_seed(seed: int = 2020) -> None:
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)


def get_recommendations_context(recommendations, start_rank=1):
    global inters
    rec_context = list()

    def round_list(float_list, to=5):
        return [round(num, to) for num in float_list]

    if inters is None:
        inters = dict(zip(*np.unique(pd.read_csv(f"{RECSYS_DATA}/lastfm_recbole/lastfm_recbole.inter", sep='\t')[
                      'track_id:token'], return_counts=True)))

    for rank, (score, rec_id) in enumerate(recommendations):
        placeholder = 4 * ['']
        track = get_track(rec_id)
        _, title, artist_id, album_id, vadst = track
        _, artist, artist_vadst = get_artist(artist_id)
        if album_id:
            _, album, _, album_vadst = get_album(album_id)
            album_tags = get_album_tags(album_id)
        track_tags = get_track_tags(rec_id)
        artist_tags = get_artist_tags(artist_id)

        r_data = {
            'id':             rec_id,
            'title':          title,
            'rank':           start_rank + rank,
            'score':          round(float(score), 5) if score else 'None',
            'artist':         [artist, artist_tags, round_list(artist_vadst) or placeholder],
            'album':          [album,  album_tags,  round_list(album_vadst) or placeholder] if album_id else None,
            'tags':           track_tags,
            'vadst':          round_list(vadst) or placeholder,
            'users_listened': inters[int(rec_id)],
            'preview_url':    f"{reverse('lastfm_preview')}?artist={quote(artist)}&title={quote(title)}&lyrics=on"
        }
        rec_context.append(r_data)
    return rec_context


def scores_to_recommendations(scores, cutoff):
    if isinstance(scores, torch.Tensor):
        scores = scores.cpu().numpy().flatten()

    item_ids = RECSYS_DATASET.id2token(
        RECSYS_DATASET.iid_field, list(range(RECSYS_DATASET.item_num)))

    sorted_idx = np.argsort(-scores)
    return list(zip(scores[sorted_idx], item_ids[sorted_idx]))[:cutoff]


def get_recommendations_by_user(username, model, predict_args=dict(), cutoff=10):
    original_id = get_user_id(username)
    uid = original_id or "1"

    uid_series = RECSYS_DATASET.token2id(RECSYS_DATASET.uid_field, [str(uid)])

    scores = model.full_sort_predict(
        {RECSYS_DATASET.uid_field: uid_series}, **predict_args)
    recs = scores_to_recommendations(scores, cutoff)

    return original_id, recs


def get_recommendations_by_tags(tags, cutoff):
    def process_tag(tag):
        # Strip spaces and hyphens
        tag = tag.replace(' ', '').replace('-', '')
        try:
            return RECSYS_DATASET.token2id("tags", tag)
        except ValueError:
            return -1

    tags_ids = [process_tag(tag) for tag in tags]

    # Multiply tags based on position, group into single vector
    grouped_tags = list()
    for i, tag_id in enumerate(tags_ids):
        grouped_tags += [tag_id] * (len(tags)-i)

    scores = RECSYS_MODELS['cosine'][1].feature_cosine_scores([grouped_tags])

    recs = scores_to_recommendations(scores, cutoff)

    return recs


def load_model(model, config=dict(), use_training=False):
    global RECSYS_DATASET

    config['dataset_save_path'] = 'backend/research/recbole_research/saved/lastfm_recbole-dataset.pth'
    config['save_dataloaders'] = False
    config['load_col'] = {
        'inter': ['user_id', 'track_id', 'rating', 'timestamp'],
        'item': ['track_id', 'artist_id', 'album_id', 'tags', 'vadst'],
        'user': ['user_id']
    }

    config, recommender, dataset, _, _, _ = load_data_and_model(
        load_model=model,
        preload_dataset=RECSYS_DATASET,
        update_config=config,
        use_training=use_training
    )

    if not RECSYS_DATASET:
        RECSYS_DATASET = dataset

    return recommender

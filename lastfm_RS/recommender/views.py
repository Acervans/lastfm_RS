from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.urls import reverse
from django.core.paginator import Paginator

from .forms import *
from bs4 import BeautifulSoup
from recbole.data.dataset import Interaction
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

DF_DATASET = None  # Features in DataFrames
IA_DATASET = None  # Features in Interactions

# Loaded Models ID: [MODEL, DEVICE]
RECSYS_MODELS = dict()

TABLES_COUNT = get_tables_count()

# GLOBAL STORAGE
recs_context = dict()
user_data = dict()
inters = None


def index(request: HttpRequest) -> HttpResponse:
    """ View function for LastMood's home page

    Args:
        request (HttpRequest): User request object

    Returns:
        HttpResponse: Response to requested resources
    """
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    if 'useralltracks' not in TABLES_COUNT:
        TABLES_COUNT['useralltracks'] = TABLES_COUNT['usertoptracks'] + \
            TABLES_COUNT['userrecenttracks'] + TABLES_COUNT['userlovedtracks']

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={
            'num_visits': num_visits,
            'stats': TABLES_COUNT,
        },
    )


def register(request: HttpRequest) -> HttpResponse:
    """ View function for user registration

    Args:
        request (HttpRequest): User request object

    Returns:
        HttpResponse: Response to requested resources
    """
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


def lastfm_preview(request: HttpRequest) -> HttpResponse:
    """ View function for the Last.fm Track Previewer

    Args:
        request (HttpRequest): User request object

    Returns:
        HttpResponse: Response to requested resources
    """
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


def get_track_context(artist: str, title: str, do_lyrics: bool) -> dict:
    """ Gets information from a track for the Track Previewer

    Args:
        artist (str): Artist of the track
        title (str): Title of the track
        do_lyrics (bool): Search track lyrics with the Genius API

    Returns:
        dict: Relevant context of the track
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

        # Get playlinks for youtube and spotify embeds
        if plinks:
            yt_tag = plinks.find(
                'a', {'class': 'play-this-track-playlink--youtube'})
            if yt_tag:
                yt_id = yt_tag.get('data-youtube-id')

            sp_tag = plinks.find(
                'a', {'class': 'play-this-track-playlink--spotify'})
            if sp_tag:
                sp_id = sp_tag.get('href').rsplit('track/')[1]

        # Get lyrics from Genius API
        if do_lyrics:
            while True:
                try:
                    gsong = GENIUS.search_song(
                        title, artist, get_full_info=False)
                    break
                except TypeError:
                    continue
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


def vad_analysis(request: HttpRequest) -> HttpResponse:
    """ View function for the VAD Analyzer

    Args:
        request (HttpRequest): User request object

    Returns:
        HttpResponse: Response to requested resources
    """
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


def user_scraper(request: HttpRequest) -> HttpResponse:
    """ View function for the Last.fm User Scraper

    Args:
        request (HttpRequest): User request object

    Returns:
        HttpResponse: Response to requested resources
    """
    global user_data

    user_data[request.session._get_or_create_session_key()] = dict()

    form = UserScraperForm()
    if request.method == 'GET' and 'username' in request.GET:
        form = UserScraperForm(request.GET)
        if form.is_valid():
            items = ['tracks', 'artists', 'albums', 'tags']
            username = form.cleaned_data.get('username')
            anonymous = form.cleaned_data.get('anonymous')
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
                        'alias':    'Random User' if anonymous else username,
                        'user_url': PYLAST.get_user(username).get_url()
                    },
                )
    return render(request, 'user_scraper_form.html', context={'form': form})


def scrape_items(request: HttpRequest,
                 keys:    list[str],
                 include: str) -> JsonResponse:
    """ Scrapes user items based on request and data keys (asynchronous)

    Args:
        request (HttpRequest): User request object
        keys (list[str]): Keys to access relevant scraped data
        include (str): Item type to include in the scraping

    Returns:
        JsonResponse: Response with scraped data
    """
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


def scrape_tracks(request: HttpRequest) -> JsonResponse:
    """ Scrapes recent, loved and top tracks from a user """
    return scrape_items(
        request,
        keys=['recent_tracks', 'loved_tracks', 'top_tracks'],
        include='tracks'
    )


def scrape_artists(request: HttpRequest) -> JsonResponse:
    """ Scrapes top artists from a user """
    return scrape_items(
        request,
        keys=['top_artists'],
        include='artists'
    )


def scrape_albums(request: HttpRequest) -> JsonResponse:
    """ Scrapes top albums from a user """
    return scrape_items(
        request,
        keys=['top_albums'],
        include='albums'
    )


def scrape_tags(request: HttpRequest) -> JsonResponse:
    """ Scrapes items' top tags from a user """
    return scrape_items(
        request,
        keys=['tags_count', 'item_tags'],
        include='tags'
    )


def recommendations(request: HttpRequest) -> HttpResponse:
    """ View function for the Track Recommender

    Args:
        request (HttpRequest): User request object

    Returns:
        HttpResponse: Response to requested resources
    """
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
            model_name = dict(rec_form.fields['model'].choices)[recsys]
            username = url_user = rec_form.cleaned_data.get('username')
            cutoff = rec_form.cleaned_data.get('cutoff')
            limit = rec_form.cleaned_data.get('limit')
            non_personalized = recsys in ('random', 'pop', 'search')
            predict_args = dict()
            scraper_url = anon = None

            uid = get_user_id(username)
            if not uid:
                set_seed(None)
                uid = np.random.randint(1, TABLES_COUNT['user_'] + 1)
                if non_personalized:
                    url_user = None
                else:
                    url_user = get_username(uid)
                    username = 'Random User'
                    anon = True

            model_path = f'{SAVED_PATH}/{recsys}.pth'
            try:
                match recsys:
                    case 'random':
                        recsys_form = RandomRecommenderForm(
                            request.GET, prefix='random')
                        if recsys_form.is_valid():
                            seed = recsys_form.cleaned_data.get('seed')
                            seed = seed if seed is not None else int(
                                np.random.randint(2**32 - 1))
                            predict_args = {'generate_new': True}

                            if recsys not in RECSYS_MODELS:
                                RECSYS_MODELS[recsys] = load_model(model_path, config={
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

                            RECSYS_MODELS[recsys] = load_model(model_path, config={
                                'weighted_average': weighted,
                                'knn_topk': topk if topk else None,
                                'Vectorizer_Config': {
                                    'binary': binary
                                }
                            })

                            if tags:
                                tags = tags.split(',')
                                recs = get_recommendations_by_tags(
                                    tags, cutoff)
                                username = ' + '.join(
                                    map(lambda x: f"'{x}'", tags))
                                url_user = None

                    case 'search':
                        recsys_form = SearchForm(
                            request.GET, prefix='search')
                        if recsys_form.is_valid():
                            by = ('Track', 'Artist', 'Album')
                            track_query, artist_query, album_query = queries = [
                                recsys_form.cleaned_data.get(f'query_{x.lower()}') for x in by]
                            by_labels = [f"{x} Query '{q}'" for i, x in enumerate(
                                by) if (q := queries[i])]
                            username = ' + '.join(by_labels)

                            tracks = search_tracks(
                                track_query, artist_query, album_query, min(cutoff, 2**63 - 1))
                            recs = list(map(lambda t: (None, t), tracks))

                    case _:
                        if recsys not in RECSYS_MODELS:
                            RECSYS_MODELS[recsys] = load_model(
                                model_path, recbole_model=True)

                if recs is None:
                    recs = get_recommendations_by_user(
                        user_id=uid,
                        model=RECSYS_MODELS[recsys][0],
                        device=RECSYS_MODELS[recsys][1],
                        predict_args=predict_args,
                        cutoff=cutoff
                    )

                    if url_user:
                        scraper_url = f"{reverse('user_scraper')}?username={quote(url_user)}" \
                            "&use_database=on" \
                            "&include_tracks=on" \
                            "&include_artists=on" \
                            "&include_albums=on" \
                            "&include_tags=on"
                        if anon:
                            scraper_url += '&anonymous=on'

                if not limit:
                    limit = cutoff

                p = Paginator(recs, limit)
                first_page = p.page(1)

                recs_context[session_key] = {
                    'username': username,
                    'scraper_url': scraper_url,
                    'model': model_name,
                    'recommendations': get_recommendations_context(first_page.object_list),
                    'is_paginated': limit and limit < cutoff,
                    'paginator': p,
                    'page_obj': first_page,
                    'page_range': p.get_elided_page_range(1)
                }

                return render(request, 'lastfm_recommend.html', context=recs_context[session_key])

            except FileNotFoundError:
                rec_form.add_error('model', f'{model_name} is unavailable')

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
    """ Sets the RNG seed or randomizes it

    Args:
        seed (int): Seed value

    Returns:
        None
    """
    if seed:
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
    else:
        np.random.seed()
        torch.seed()
        torch.cuda.seed()


def get_recommendations_context(recommendations: list[tuple], start_rank: int = 1) -> list[dict]:
    """ Obtains relevant context data for recommended tracks

    Args:
        recommendations (list[tuple]): Recommendations (score, track_id)
        start_rank (int): Starting rank for the list, used with pagination

    Returns:
        list[dict]: Relevant context for each recommendation
    """
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


def scores_to_recommendations(scores: torch.Tensor | np.ndarray, cutoff: int) -> list[tuple]:
    """ Assigns respective tracks to the generated scores

    Args:
        scores (torch.Tensor | np.ndarray): Tracks' scores
        cutoff (int): Number of tracks to recommend

    Returns:
        list[tuple]: Recommendations (score, track_id)
    """
    if isinstance(scores, torch.Tensor):
        scores = scores.cpu().numpy().flatten()
    scores = scores[1:]

    item_ids = DF_DATASET.id2token(
        DF_DATASET.iid_field, list(range(1, DF_DATASET.item_num)))

    sorted_idx = np.argsort(scores)[:-(cutoff + 1):-1]
    return list(zip(scores[sorted_idx], item_ids[sorted_idx]))


def get_recommendations_by_user(user_id:      int,
                                model:        torch.nn.Module,
                                device:       torch.device,
                                predict_args: dict = dict(),
                                cutoff:       int = 10) -> list[tuple]:
    """ Obtains recommendations for a given user using the selected model

    Args:
        user_id (int): ID of user to get recommendations for
        model (torch.nn.Module): Recommendation model
        device (torch.device): Device where the model is loaded
        predict_args (dict): Additional recommendation arguments
        cutoff (int): Number of tracks to recommend

    Returns:
        list[tuple]: Recommendations (score, track_id)
    """
    uid_series = DF_DATASET.token2id(
        DF_DATASET.uid_field, [str(user_id)])

    model.eval()
    uid_inter = {DF_DATASET.uid_field: uid_series}
    try:
        scores = model.full_sort_predict(uid_inter, **predict_args)
    except NotImplementedError:
        scores = full_sort_scores(model, device, uid_inter)

    recs = scores_to_recommendations(scores, cutoff)

    return recs


def get_recommendations_by_tags(tags: list[str], cutoff: int) -> list[tuple]:
    """ Obtains recommendations based on similarities of chosen tags

    Args:
        tags (list[str]): Tags to obtain similar tracks from
        cutoff (int): Number of tracks to recommend

    Returns:
        list[tuple]: Recommendations (score, track_id)
    """
    def process_tag(tag: str):
        """ Preprocess tag and obtain token ID """
        # Strip spaces and hyphens
        tag = tag.replace(' ', '').replace('-', '')
        try:
            # Internal token ID
            return DF_DATASET.token2id("tags", tag)
        except ValueError:
            return -1

    tags_ids = [process_tag(tag) for tag in tags]

    # Multiply tags based on position, group into single vector
    grouped_tags = list()
    for i, tag_id in enumerate(tags_ids):
        grouped_tags += [tag_id] * (len(tags)-i)

    scores = RECSYS_MODELS['cosine'][0].feature_cosine_scores([grouped_tags])

    recs = scores_to_recommendations(scores, cutoff)

    return recs


def full_sort_scores(model:      torch.nn.Module,
                     device:     torch.device,
                     uid_inter:  dict,
                     batch_size: int = 4096) -> np.ndarray:
    """ Predicts scores of all tracks for a given user

    Args:
        model (torch.nn.Module): Recommendation model
        device (torch.device): Device where the model is loaded
        uid_inter (dict): Internal user ID mapping
        batch_size (int): Number of items to process at once

    Returns:
        np.ndarray: Predicted track scores
    """
    item_feats = IA_DATASET.get_item_feature()
    scores = list()
    for i in range(0, IA_DATASET.item_num, batch_size):
        interaction = Interaction(uid_inter)
        item_feat = item_feats[i:i + batch_size]
        interaction = interaction.repeat_interleave(len(item_feat))
        interaction.update(item_feat.repeat(1))
        scores.append(model.predict(
            interaction.to(device)).detach().cpu().numpy())
    return np.concatenate(scores)


def load_model(model:         str,
               config:        dict = dict(),
               recbole_model: bool = False) -> tuple[torch.nn.Module, torch.device]:
    """ Loads the recommendation model (and required datasets) lazily

    Args:
        model (str): Path to pre-trained model
        config (dict): Additional loading configurations
        recbole_model (bool): Whether the model was implemented by RecBole

    Returns:
        tuple[torch.nn.Module, torch.device]: Model and device where it's loaded
    """
    global DF_DATASET

    def _lazy_dataset():
        """ Selects the recommendation dataset, loading it if needed """
        global IA_DATASET

        if recbole_model:
            if not IA_DATASET and DF_DATASET:
                IA_DATASET = DF_DATASET.copy(DF_DATASET.inter_feat)
                # Converts DataFrames into Interactions
                IA_DATASET.build()
            return IA_DATASET
        return DF_DATASET

    config['dataset_save_path'] = f'{SAVED_PATH}/lastfm_recbole-dataset.pth'
    config['save_dataloaders'] = False
    config['load_col'] = {
        'inter': ['user_id', 'track_id', 'rating', 'timestamp'],
        'item': ['track_id', 'artist_id', 'tags', 'v', 'a', 'd', 'stsc'],
        'user': ['user_id']
    }

    preload_dataset = _lazy_dataset()
    config, recommender, DF_DATASET, _, _, _ = load_data_and_model(
        load_model=model,
        preload_dataset=preload_dataset,
        update_config=config,
    )

    if not preload_dataset:
        _lazy_dataset()

    return recommender, config['device']

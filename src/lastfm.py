import pylast

network = pylast.LastFMNetwork('23ff8e4c454cbb8ae4a13440bc0fa745', 'a5efd0d4bbeed8c37b0c4bd7672edf58')

kb = pylast.Artist('Kudasaibeats', network)
for x in kb.get_top_tags():
    print(x.item.get_name())
print(kb.get_bio_summary())
# Maybe use some tags + bio summary to evaluate VAD of an artist
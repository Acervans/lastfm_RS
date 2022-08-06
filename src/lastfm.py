import pylast

network = pylast.LastFMNetwork('23ff8e4c454cbb8ae4a13440bc0fa745', 'a5efd0d4bbeed8c37b0c4bd7672edf58')
pl = pylast.Track('potsu', "just friends", network)

print(pl.get_top_tags())
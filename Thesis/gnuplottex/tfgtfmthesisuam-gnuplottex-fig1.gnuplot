set terminal epslatex
set output 'gnuplottex/tfgtfmthesisuam-gnuplottex-fig1.tex'
    set key box top left
    set key width 3
    set size 0.75,0.75
    set sample 1000
    set xr [-5:5]
    set yr [-1:1]
    plot  sin(x)
  

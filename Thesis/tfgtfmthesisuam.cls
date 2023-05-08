\NeedsTeXFormat{LaTeX2e}[1994/06/01]
\ProvidesClass{tfgtfmthesisuam}[2018/06/01 v3.0 tfgtfmthesisuam class (EA)]
\typeout{Class: tfgtfmthesisuam v3.0 <2018/06/01> (Eloy Anguiano)}

%TODO: más gráficas, viudas y huérfanas

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                 Control variables                %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newif\if@nineptbool 		\@nineptboolfalse
\newif\if@tenptbool 		\@tenptboolfalse
\newif\if@elevenptbool 		\@elevenptbooltrue

\newif\if@gnuplotbool 		\@gnuplotboolfalse
\newif\if@overleafbool 		\@overleafboolfalse

\newif\if@languagespa 		\@languagespafalse

\newif\if@algorithmsbool		\@algorithmsboolfalse
\newif\if@codesbool			\@codesboolfalse
\newif\if@equationsbool		\@equationsboolfalse
\newif\if@figuresbool		\@figuresboolfalse
\newif\if@tablesbool		\@tablesboolfalse
\newif\if@textboxesbool		\@textboxesboolfalse
\newif\if@alllistsbool		\@alllistsbooltrue
\newif\if@nonelistbool		\@nonelistboolfalse

\newif\if@fullindexbool		\@fullindexboolfalse
\newif\if@extendedindexbool		\@extendedindexboolfalse
\newif\if@oldtfgtitlepagebool		\@oldtfgtitlepagebooltrue


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                  Color variables                 %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newif\if@uambool 		\@uambooltrue
\newif\if@blackcolorbool 	\@blackcolorboolfalse
\newif\if@graycolorbool 	\@graycolorboolfalse
\newif\if@redcolorbool 		\@redcolorboolfalse
\newif\if@greencolorbool 	\@greencolorboolfalse
\newif\if@bluecolorbool 	\@bluecolorboolfalse
\newif\if@yellowcolorbool 	\@yellowcolorboolfalse
\newif\if@magentacolorbool 	\@magentacolorboolfalse
\newif\if@cyancolorbool 	\@cyancolorboolfalse
\newif\if@orangecolorbool 	\@orangecolorboolfalse
\newif\if@cienciasbool \@cienciasboolfalse
\newif\if@economicasbool \@economicasboolfalse
\newif\if@derechobool \@derechoboolfalse
\newif\if@filosofiabool \@filosofiaboolfalse
\newif\if@profesoradobool \@profesoradoboolfalse
\newif\if@medicinabool \@medicinaboolfalse
\newif\if@psicologiabool \@psicologiaboolfalse
\newif\if@epsbool \@epsboolfalse
\newif\if@enfermeriabool \@enfermeriaboolfalse
\newif\if@fisioterapiabool \@fisioterapiaboolfalse

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                 Struct variables                 %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newif\if@finalmodebool \@finalmodeboolfalse
\newif\if@printmodebool \@printmodeboolfalse

\newif\if@firstchappagnumbool 	\@firstchappagnumboolfalse
\newif\if@gotfirstpage 			\@gotfirstpagefalse
\newif\if@rstnum 				\@rstnumfalse
\newif\if@preambletext 			\@preambletexttrue

\newif\if@coadvisorbool \@coadvisorboolfalse
\newif\if@tfgwork \@tfgworktrue
\newif\if@tfmwork \@tfmworkfalse
\newif\if@thesiswork \@thesisworkfalse
\newif\if@coversbool \@coversboolfalse

\newif\if@copyrightbool \@copyrightbooltrue
\newif\if@copyleftbool \@copyleftboolfalse

\newif\if@bibliographymodebool \@bibliographymodeboolfalse
\newif\if@appendixbool \@appendixboolfalse

\newif\if@firstlistprintedbool \@firstlistprintedboolfalse
\newif\if@logosdirbool \@logosdirboolfalse

\newif\if@subtitlebool \@subtitleboolfalse

\newif\if@jupyterbool \@jupyterboolfalse

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                  Control options                 %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\DeclareOption{normalbook}{\@nineptboolfalse \@tenptboolfalse \@elevenptbooltrue}
\DeclareOption{smallbook}{\@nineptbooltrue \@tenptboolfalse \@elevenptboolfalse}
\DeclareOption{tinybook}{\@nineptboolfalse \@tenptbooltrue \@elevenptboolfalse}

\DeclareOption{gnuplot}{\@gnuplotbooltrue}
\DeclareOption{overleaf}{\@overleafbooltrue}

% Language options

\DeclareOption{english}{\PassOptionsToPackage{english}{babel} \PassOptionsToPackage{english}{cleveref} \@languagespafalse}
\DeclareOption{spanish}{\PassOptionsToPackage{spanish}{babel} \PassOptionsToPackage{spanish}{cleveref} \@languagespatrue}

% Numbering options

\DeclareOption{firstnumbered}{\@firstchappagnumbooltrue}

% Color options

\DeclareOption{printcolors}{\@printcolorsbooltrue}

\DeclareOption{uambased}{\@uambooltrue}
\DeclareOption{blackbased}{\@uamboolfalse \@blackcolorbooltrue}
\DeclareOption{graybased}{\@uamboolfalse \@graycolorbooltrue}
\DeclareOption{redbased}{\@uamboolfalse \@redcolorbooltrue}
\DeclareOption{greenbased}{\@uamboolfalse \@greencolorbooltrue}
\DeclareOption{bluebased}{\@uamboolfalse \@bluecolorbooltrue}
\DeclareOption{yellowbased}{\@uamboolfalse \@yellowcolorbooltrue}
\DeclareOption{magentabased}{\@uamboolfalse \@magentacolorbooltrue}
\DeclareOption{cyanbased}{\@uamboolfalse \@cyancolorbooltrue}
\DeclareOption{orangebased}{\@uamboolfalse \@orangecolorbooltrue}
\DeclareOption{cienciasbased}{\@uamboolfalse \@cienciasbooltrue}
\DeclareOption{economicasbased}{\@uamboolfalse \@economicasbooltrue}
\DeclareOption{derechobased}{\@uamboolfalse \@derechobooltrue}
\DeclareOption{filosofiabased}{\@uamboolfalse \@filosofiabooltrue}
\DeclareOption{profesoradobased}{\@uamboolfalse \@profesoradobooltrue}
\DeclareOption{medicinabased}{\@uamboolfalse \@medicinabooltrue}
\DeclareOption{psicologiabased}{\@uamboolfalse \@psicologiabooltrue}
\DeclareOption{epsbased}{\@uamboolfalse \@epsbooltrue}
\DeclareOption{enfermeriabased}{\@uamboolfalse \@enfermeriabooltrue}
\DeclareOption{fisioterapiabased}{\@uamboolfalse \@fisioterapiabooltrue}

% Struct control

\DeclareOption{tfg}{\@thesisworkfalse \@tfmworkfalse \@tfgworktrue}
\DeclareOption{newtfg}{\@thesisworkfalse \@tfmworkfalse \@tfgworktrue}
\DeclareOption{tfm}{\@thesisworkfalse \@tfmworktrue \@tfgworkfalse}
\DeclareOption{thesis}{\@thesisworktrue \@tfmworkfalse \@tfgworkfalse}
\DeclareOption{final}{\@finalmodebooltrue}
\DeclareOption{printable}{\@printmodebooltrue}
\DeclareOption{covers}{\@coversbooltrue}

\DeclareOption{copyright}{\@copyleftboolfalse \@copyrightbooltrue}
\DeclareOption{copyleft}{\@copyleftbooltrue \@copyrightboolfalse}
\DeclareOption{nocopyright}{\@copyleftboolfalse \@copyrightboolfalse}

\DeclareOption{nonelo}{\@alllistsboolfalse \@nonelistbooltrue}
\DeclareOption{loa}{\@algorithmsbooltrue \@alllistsboolfalse \@nonelistboolfalse}
\DeclareOption{loc}{\@codesbooltrue \@alllistsboolfalse \@nonelistboolfalse}
\DeclareOption{loe}{\@equationsbooltrue \@alllistsboolfalse \@nonelistboolfalse}
\DeclareOption{lof}{\@figuresbooltrue \@alllistsboolfalse \@nonelistboolfalse}
\DeclareOption{lot}{\@tablesbooltrue \@alllistsboolfalse \@nonelistboolfalse}
\DeclareOption{lotb}{\@textboxesbooltrue \@alllistsboolfalse \@nonelistboolfalse}

\DeclareOption{normalindex}{\@extendedindexboolfalse \@fullindexboolfalse}
\DeclareOption{extendedindex}{\@extendedindexbooltrue}
\DeclareOption{fullindex}{\@fullindexbooltrue}

\DeclareOption{jupyter}{\@jupyterbooltrue}


% Process and default options

\ExecuteOptions{spanish}
\ProcessOptions\relax

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                     Packages                     %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\LoadClass[makeidx]{book}

\@ifpackageloaded{inputenc}{\PassOptionsToPackage{utf8x}{inputenc}}{\RequirePackage[utf8x]{inputenc}} % Codificación
\@ifpackageloaded{babel}{}{\RequirePackage{babel}} % Language settings
\@ifpackageloaded{amsmath}{}{\RequirePackage{amsmath}} % Math settings
\@ifpackageloaded{amssymb}{}{\RequirePackage{amssymb}} % Math settings
\@ifpackageloaded{fancyhdr}{}{\RequirePackage{fancyhdr}} % Headers
\@ifpackageloaded{fancybox}{}{\RequirePackage{fancybox}} % Fancy put and boxes
\@ifpackageloaded{caption}{\PassOptionsToPackage{small,bf,margin={0.0592\paperheight,0.0592\paperheight}}{caption}}{\RequirePackage[small,bf,margin={0.0592\paperheight,0.0592\paperheight}]{caption}} % Caption style
\@ifpackageloaded{subfigure}{\PassOptionsToPackage{hang,TABBOTCAP}{subfigure}}{\RequirePackage[hang,TABBOTCAP]{subfigure}} % For subfigure
\@ifpackageloaded{tocloft}{\PassOptionsToPackage{subfigure}{tocloft}}{\RequirePackage[subfigure]{tocloft}} % Some list of XXX
\@ifpackageloaded{float}{}{\RequirePackage{float}} % Float environments
\@ifpackageloaded{listings}{}{\RequirePackage{listings}} % Code formating
\@ifpackageloaded{cite}{}{\RequirePackage{cite}} % Compresing bibliography
\@ifpackageloaded{xcolor}{}{\RequirePackage{xcolor}}
\@ifpackageloaded{pgf}{}{\RequirePackage{pgf}} % Images and colors
\@ifpackageloaded{algorithm2e}{\PassOptionsToPackage{algo2e}{algorithm2e}}{\RequirePackage[algo2e]{algorithm2e}} % Algorithms
\@ifpackageloaded{pgfplots}{}{\RequirePackage{pgfplots}} % Scientific plots
\@ifpackageloaded{pgfgantt}{}{\RequirePackage{pgfgantt}} % Gantt plots
\if@gnuplotbool
	\@ifpackageloaded{gnuplottex}{\PassOptionsToPackage{shell,cleanup,subfolder}{gnuplottex}}{\RequirePackage[shell,cleanup,subfolder]{gnuplottex}}
\fi% Scientific plots
\if@overleafbool
	\@ifpackageloaded{glossaries}{\PassOptionsToPackage{acronyms,nogroupskip,nonumberlist,shortcuts,toc}{glossaries}}{\RequirePackage[acronyms,nogroupskip,nonumberlist,shortcuts,toc]{glossaries}}
\else
	\@ifpackageloaded{glossaries}{\PassOptionsToPackage{acronyms,nogroupskip,nonumberlist,shortcuts,toc,xindy={language=spanish-traditional}}{glossaries}}{\RequirePackage[acronyms,nogroupskip,nonumberlist,shortcuts,toc,xindy={language=spanish-traditional}]{glossaries}}
\fi

\@ifpackageloaded{calc}{}{\RequirePackage{calc}}
\@ifpackageloaded{verbatim}{}{\RequirePackage{verbatim}}
\@ifpackageloaded{alltt}{}{\RequirePackage{alltt}}
\@ifpackageloaded{makeidx}{}{\RequirePackage{makeidx}}
\@ifpackageloaded{graphicx}{}{\RequirePackage{graphicx}}
\@ifpackageloaded{textcomp}{}{\RequirePackage{textcomp}}
\@ifpackageloaded{times}{}{\RequirePackage{times}}
\@ifpackageloaded{ifpdf}{}{\RequirePackage{ifpdf}}
\@ifpackageloaded{wrapfig}{}{\RequirePackage{wrapfig}}
\@ifpackageloaded{longtable}{}{\RequirePackage{longtable}}
\@ifpackageloaded{eurosym}{}{\RequirePackage{eurosym}}
\@ifpackageloaded{etoolbox}{}{\RequirePackage{etoolbox}}
\@ifpackageloaded{multicol}{}{\RequirePackage{multicol}}
\@ifpackageloaded{multirow}{}{\RequirePackage{multirow}}
\@ifpackageloaded{filecontents}{}{\RequirePackage{filecontents}}
\@ifpackageloaded{hyperref}{}{\RequirePackage{hyperref}}
\@ifpackageloaded{twoopt}{}{\RequirePackage{twoopt}}
\@ifpackageloaded{cleveref}{\PassOptionsToPackage{nameinlink,noabbrev}{cleveref}}{\RequirePackage[nameinlink,noabbrev]{cleveref}}
\@ifpackageloaded{morewrites}{}{\RequirePackage{morewrites}}
\@ifpackageloaded{etex}{}{\RequirePackage{etex}}
\@ifpackageloaded{datetime}{}{\RequirePackage{datetime}}
\@ifpackageloaded{lipsum}{}{\RequirePackage{lipsum}}
%\@ifpackageloaded{ucs}{}{\RequirePackage{[mathletters]{ucs}} % Extended unicode (utf-8) support

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%           Redefininng ex, em and pt               %%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\if@jupyterbool
	\@ifpackageloaded{mathpazo}{}{\RequirePackage{mathpazo}}
	\@ifpackageloaded{graphicx}{}{\RequirePackage{graphicx}}
	\@ifpackageloaded{adjustbox}{}{\RequirePackage{adjustbox}} % Used to constrain images to a maximum size 
	\@ifpackageloaded{enumerate}{}{\RequirePackage{enumerate}} % Needed for markdown enumerations to work
	\@ifpackageloaded{textcomp}{}{\RequirePackage{textcomp}}
    \@ifpackageloaded{upquote}{}{\RequirePackage{upquote}} % Upright quotes for verbatim code
    \@ifpackageloaded{fancyvrb}{}{\RequirePackage{fancyvrb}} % verbatim replacement that allows latex
    \@ifpackageloaded{grffile}{}{\RequirePackage{grffile}} % extends the file name processing of package graphics 
                         % to support a larger range 
    % The hyperref package gives us a pdf with properly built
    % internal navigation ('pdf bookmarks' for the table of contents,
	% internal cross-reference links, web links for URLs, etc.)
	
    \@ifpackageloaded{booktabs}{}{\RequirePackage{booktabs}}  % table support for pandoc > 1.12.2
    %\@ifpackageloaded{enumitem}{}{\RequirePackage{[inline]{enumitem}}} % IRkernel/repr support (it uses the enumerate* environment)
    %\@ifpackageloaded{ulem}{}{\RequirePackage{[normalem]{ulem}}} % ulem is needed to support strikethroughs (\sout)
                                % normalem makes italics be italics, not underlines

    \def\maxwidth{\ifdim\Gin@nat@width>\linewidth\linewidth
	\else\Gin@nat@width\fi}
	
    %\let\Oldincludegraphics\includegraphics
    %% Set max figure width to be 80% of text width, for now hardcoded.
    %\renewcommand{\includegraphics}[1]{\Oldincludegraphics[width=.8\maxwidth]{#1}}
    %% Ensure that by default, figures have no caption (until we provide a
    %% proper Figure object with a Caption API and a way to capture that
	%% in the conversion process - todo). 
	
    %\DeclareCaptionLabelFormat{nolabel}{}
    %\captionsetup{labelformat=nolabel}


    \AtBeginDocument{%
        \def\PYZsq{\textquotesingle}% Upright quotes in Pygmentized code
	}

    
    
    % Colors for the hyperref package
    %\definecolor{urlcolor}
    % Document parameters{rgb}{0,.145,.698}
    %\definecolor{linkcolor}{rgb}{.71,0.21,0.01}
    %\definecolor{citecolor}{rgb}{.12,.54,.11}

    % ANSI colors
    \definecolor{ansi-black}{HTML}{3E424D}
    \definecolor{ansi-black-intense}{HTML}{282C36}
    \definecolor{ansi-red}{HTML}{E75C58}
    \definecolor{ansi-red-intense}{HTML}{B22B31}
    \definecolor{ansi-green}{HTML}{00A250}
    \definecolor{ansi-green-intense}{HTML}{007427}
    \definecolor{ansi-yellow}{HTML}{DDB62B}
    \definecolor{ansi-yellow-intense}{HTML}{B27D12}
    \definecolor{ansi-blue}{HTML}{208FFB}
    \definecolor{ansi-blue-intense}{HTML}{0065CA}
    \definecolor{ansi-magenta}{HTML}{D160C4}
    \definecolor{ansi-magenta-intense}{HTML}{A03196}
    \definecolor{ansi-cyan}{HTML}{60C6C8}
    \definecolor{ansi-cyan-intense}{HTML}{258F8F}
    \definecolor{ansi-white}{HTML}{C5C1B4}
	\definecolor{ansi-white-intense}{HTML}{A1A6B2}
	\def\verbatim@font{\txtfont}
	\DefineVerbatimEnvironment{Highlighting}{Verbatim}{commandchars=\\\{\},fontsize=\footnotesize}
	\def\verbatim@font{\txtfont}

    % commands and environments needed by pandoc snippets
    % extracted from the output of `pandoc -s`
    \providecommand{\tightlist}{%
      \setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
    
    \newenvironment{Shaded}{}{}
    \newcommand{\KeywordTok}[1]{\textcolor[rgb]{0.00,0.44,0.13}{\textbf{{#1}}}}
    \newcommand{\DataTypeTok}[1]{\textcolor[rgb]{0.56,0.13,0.00}{{#1}}}
    \newcommand{\DecValTok}[1]{\textcolor[rgb]{0.25,0.63,0.44}{{#1}}}
    \newcommand{\BaseNTok}[1]{\textcolor[rgb]{0.25,0.63,0.44}{{#1}}}
    \newcommand{\FloatTok}[1]{\textcolor[rgb]{0.25,0.63,0.44}{{#1}}}
    \newcommand{\CharTok}[1]{\textcolor[rgb]{0.25,0.44,0.63}{{#1}}}
    \newcommand{\StringTok}[1]{\textcolor[rgb]{0.25,0.44,0.63}{{#1}}}
    \newcommand{\CommentTok}[1]{\textcolor[rgb]{0.38,0.63,0.69}{\textit{{#1}}}}
    \newcommand{\OtherTok}[1]{\textcolor[rgb]{0.00,0.44,0.13}{{#1}}}
    \newcommand{\AlertTok}[1]{\textcolor[rgb]{1.00,0.00,0.00}{\textbf{{#1}}}}
    \newcommand{\FunctionTok}[1]{\textcolor[rgb]{0.02,0.16,0.49}{{#1}}}
    \newcommand{\RegionMarkerTok}[1]{{#1}}
    \newcommand{\ErrorTok}[1]{\textcolor[rgb]{1.00,0.00,0.00}{\textbf{{#1}}}}
    \newcommand{\NormalTok}[1]{{#1}}
    
    % Additional commands for more recent versions of Pandoc
    \newcommand{\ConstantTok}[1]{\textcolor[rgb]{0.53,0.00,0.00}{{#1}}}
    \newcommand{\SpecialCharTok}[1]{\textcolor[rgb]{0.25,0.44,0.63}{{#1}}}
    \newcommand{\VerbatimStringTok}[1]{\textcolor[rgb]{0.25,0.44,0.63}{{#1}}}
    \newcommand{\SpecialStringTok}[1]{\textcolor[rgb]{0.73,0.40,0.53}{{#1}}}
    \newcommand{\ImportTok}[1]{{#1}}
    \newcommand{\DocumentationTok}[1]{\textcolor[rgb]{0.73,0.13,0.13}{\textit{{#1}}}}
    \newcommand{\AnnotationTok}[1]{\textcolor[rgb]{0.38,0.63,0.69}{\textbf{\textit{{#1}}}}}
    \newcommand{\CommentVarTok}[1]{\textcolor[rgb]{0.38,0.63,0.69}{\textbf{\textit{{#1}}}}}
    \newcommand{\VariableTok}[1]{\textcolor[rgb]{0.10,0.09,0.49}{{#1}}}
    \newcommand{\ControlFlowTok}[1]{\textcolor[rgb]{0.00,0.44,0.13}{\textbf{{#1}}}}
    \newcommand{\OperatorTok}[1]{\textcolor[rgb]{0.40,0.40,0.40}{{#1}}}
    \newcommand{\BuiltInTok}[1]{{#1}}
    \newcommand{\ExtensionTok}[1]{{#1}}
    \newcommand{\PreprocessorTok}[1]{\textcolor[rgb]{0.74,0.48,0.00}{{#1}}}
    \newcommand{\AttributeTok}[1]{\textcolor[rgb]{0.49,0.56,0.16}{{#1}}}
    \newcommand{\InformationTok}[1]{\textcolor[rgb]{0.38,0.63,0.69}{\textbf{\textit{{#1}}}}}
    \newcommand{\WarningTok}[1]{\textcolor[rgb]{0.38,0.63,0.69}{\textbf{\textit{{#1}}}}}
    
    
    % Define a nice break command that doesn't care if a line doesn't already
    % exist.
    \def\br{\hspace*{\fill} \\* }
    % Math Jax compatability definitions
    \def\gt{>}
    \def\lt{<}
    
    

    % Pygments definitions
    
	\def\PY@reset{\let\PY@it=\relax \let\PY@bf=\relax%
		\let\PY@ul=\relax \let\PY@tc=\relax%
		\let\PY@bc=\relax \let\PY@ff=\relax}
	\def\PY@tok#1{\csname PY@tok@#1\endcsname}
	\def\PY@toks#1+{\ifx\relax#1\empty\else%
		\PY@tok{#1}\expandafter\PY@toks\fi}
	\def\PY@do#1{\PY@bc{\PY@tc{\PY@ul{%
		\PY@it{\PY@bf{\PY@ff{#1}}}}}}}
	\def\PY#1#2{\PY@reset\PY@toks#1+\relax+\PY@do{#2}}

	\expandafter\def\csname PY@tok@w\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.73,0.73,0.73}{##1}}}
	\expandafter\def\csname PY@tok@c\endcsname{\let\PY@it=\textit\def\PY@tc##1{\textcolor[rgb]{0.25,0.50,0.50}{##1}}}
	\expandafter\def\csname PY@tok@cp\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.74,0.48,0.00}{##1}}}
	\expandafter\def\csname PY@tok@k\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.00,0.50,0.00}{##1}}}
	\expandafter\def\csname PY@tok@kp\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.00,0.50,0.00}{##1}}}
	\expandafter\def\csname PY@tok@kt\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.69,0.00,0.25}{##1}}}
	\expandafter\def\csname PY@tok@o\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.40,0.40,0.40}{##1}}}
	\expandafter\def\csname PY@tok@ow\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.67,0.13,1.00}{##1}}}
	\expandafter\def\csname PY@tok@nb\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.00,0.50,0.00}{##1}}}
	\expandafter\def\csname PY@tok@nf\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.00,0.00,1.00}{##1}}}
	\expandafter\def\csname PY@tok@nc\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.00,0.00,1.00}{##1}}}
	\expandafter\def\csname PY@tok@nn\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.00,0.00,1.00}{##1}}}
	\expandafter\def\csname PY@tok@ne\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.82,0.25,0.23}{##1}}}
	\expandafter\def\csname PY@tok@nv\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.10,0.09,0.49}{##1}}}
	\expandafter\def\csname PY@tok@no\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.53,0.00,0.00}{##1}}}
	\expandafter\def\csname PY@tok@nl\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.63,0.63,0.00}{##1}}}
	\expandafter\def\csname PY@tok@ni\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.60,0.60,0.60}{##1}}}
	\expandafter\def\csname PY@tok@na\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.49,0.56,0.16}{##1}}}
	\expandafter\def\csname PY@tok@nt\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.00,0.50,0.00}{##1}}}
	\expandafter\def\csname PY@tok@nd\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.67,0.13,1.00}{##1}}}
	\expandafter\def\csname PY@tok@s\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.73,0.13,0.13}{##1}}}
	\expandafter\def\csname PY@tok@sd\endcsname{\let\PY@it=\textit\def\PY@tc##1{\textcolor[rgb]{0.73,0.13,0.13}{##1}}}
	\expandafter\def\csname PY@tok@si\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.73,0.40,0.53}{##1}}}
	\expandafter\def\csname PY@tok@se\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.73,0.40,0.13}{##1}}}
	\expandafter\def\csname PY@tok@sr\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.73,0.40,0.53}{##1}}}
	\expandafter\def\csname PY@tok@ss\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.10,0.09,0.49}{##1}}}
	\expandafter\def\csname PY@tok@sx\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.00,0.50,0.00}{##1}}}
	\expandafter\def\csname PY@tok@m\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.40,0.40,0.40}{##1}}}
	\expandafter\def\csname PY@tok@gh\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.00,0.00,0.50}{##1}}}
	\expandafter\def\csname PY@tok@gu\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.50,0.00,0.50}{##1}}}
	\expandafter\def\csname PY@tok@gd\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.63,0.00,0.00}{##1}}}
	\expandafter\def\csname PY@tok@gi\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.00,0.63,0.00}{##1}}}
	\expandafter\def\csname PY@tok@gr\endcsname{\def\PY@tc##1{\textcolor[rgb]{1.00,0.00,0.00}{##1}}}
	\expandafter\def\csname PY@tok@ge\endcsname{\let\PY@it=\textit}
	\expandafter\def\csname PY@tok@gs\endcsname{\let\PY@bf=\textbf}
	\expandafter\def\csname PY@tok@gp\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.00,0.00,0.50}{##1}}}
	\expandafter\def\csname PY@tok@go\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.53,0.53,0.53}{##1}}}
	\expandafter\def\csname PY@tok@gt\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.00,0.27,0.87}{##1}}}
	\expandafter\def\csname PY@tok@err\endcsname{\def\PY@bc##1{\setlength{\fboxsep}{0pt}\fcolorbox[rgb]{1.00,0.00,0.00}{1,1,1}{\strut ##1}}}
	\expandafter\def\csname PY@tok@kc\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.00,0.50,0.00}{##1}}}
	\expandafter\def\csname PY@tok@kd\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.00,0.50,0.00}{##1}}}
	\expandafter\def\csname PY@tok@kn\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.00,0.50,0.00}{##1}}}
	\expandafter\def\csname PY@tok@kr\endcsname{\let\PY@bf=\textbf\def\PY@tc##1{\textcolor[rgb]{0.00,0.50,0.00}{##1}}}
	\expandafter\def\csname PY@tok@bp\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.00,0.50,0.00}{##1}}}
	\expandafter\def\csname PY@tok@fm\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.00,0.00,1.00}{##1}}}
	\expandafter\def\csname PY@tok@vc\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.10,0.09,0.49}{##1}}}
	\expandafter\def\csname PY@tok@vg\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.10,0.09,0.49}{##1}}}
	\expandafter\def\csname PY@tok@vi\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.10,0.09,0.49}{##1}}}
	\expandafter\def\csname PY@tok@vm\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.10,0.09,0.49}{##1}}}
	\expandafter\def\csname PY@tok@sa\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.73,0.13,0.13}{##1}}}
	\expandafter\def\csname PY@tok@sb\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.73,0.13,0.13}{##1}}}
	\expandafter\def\csname PY@tok@sc\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.73,0.13,0.13}{##1}}}
	\expandafter\def\csname PY@tok@dl\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.73,0.13,0.13}{##1}}}
	\expandafter\def\csname PY@tok@s2\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.73,0.13,0.13}{##1}}}
	\expandafter\def\csname PY@tok@sh\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.73,0.13,0.13}{##1}}}
	\expandafter\def\csname PY@tok@s1\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.73,0.13,0.13}{##1}}}
	\expandafter\def\csname PY@tok@mb\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.40,0.40,0.40}{##1}}}
	\expandafter\def\csname PY@tok@mf\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.40,0.40,0.40}{##1}}}
	\expandafter\def\csname PY@tok@mh\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.40,0.40,0.40}{##1}}}
	\expandafter\def\csname PY@tok@mi\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.40,0.40,0.40}{##1}}}
	\expandafter\def\csname PY@tok@il\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.40,0.40,0.40}{##1}}}
	\expandafter\def\csname PY@tok@mo\endcsname{\def\PY@tc##1{\textcolor[rgb]{0.40,0.40,0.40}{##1}}}
	\expandafter\def\csname PY@tok@ch\endcsname{\let\PY@it=\textit\def\PY@tc##1{\textcolor[rgb]{0.25,0.50,0.50}{##1}}}
	\expandafter\def\csname PY@tok@cm\endcsname{\let\PY@it=\textit\def\PY@tc##1{\textcolor[rgb]{0.25,0.50,0.50}{##1}}}
	\expandafter\def\csname PY@tok@cpf\endcsname{\let\PY@it=\textit\def\PY@tc##1{\textcolor[rgb]{0.25,0.50,0.50}{##1}}}
	\expandafter\def\csname PY@tok@c1\endcsname{\let\PY@it=\textit\def\PY@tc##1{\textcolor[rgb]{0.25,0.50,0.50}{##1}}}
	\expandafter\def\csname PY@tok@cs\endcsname{\let\PY@it=\textit\def\PY@tc##1{\textcolor[rgb]{0.25,0.50,0.50}{##1}}}

	\def\PYZbs{\char`\\}
	\def\PYZus{\char`\_}
	\def\PYZob{\char`\{}
	\def\PYZcb{\char`\}}
	\def\PYZca{\char`\^}
	\def\PYZam{\char`\&}
	\def\PYZlt{\char`\<}
	\def\PYZgt{\char`\>}
	\def\PYZsh{\char`\#}
	\def\PYZpc{\char`\%}
	\def\PYZdl{\char`\$}
	\def\PYZhy{\char`\-}
	\def\PYZsq{\char`\'}
	\def\PYZdq{\char`\"}
	\def\PYZti{\char`\~}
	% for compatibility with earlier versions
	\def\PYZat{@}
	\def\PYZlb{[}
	\def\PYZrb{]}


    % Exact colors from NB
    \definecolor{incolor}{rgb}{0.0, 0.0, 0.5}
    \definecolor{outcolor}{rgb}{0.545, 0.0, 0.0}



    
    % Prevent overflowing lines due to hard-to-break entities
    \sloppy 
    
\fi

\newlength{\myex}
\newlength{\myem}
\newlength{\mypt}
\setlength{\myex}{0.0050950505\paperheight}
\setlength{\myem}{0.0118337374\paperheight}
\setlength{\mypt}{0.00118337374\paperheight}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                     Counters                      %%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newcounter{@ploti}

\glossaryheader
\glsgroupheading{hlabeli}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                    Variables                     %%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\def\@advisor{\mbox{}}
\def\@coadvisor{\mbox{}\@coadvisorbooltrue}
\def\@speaker{}
\def\@levelin{}
\def\@faculty{}
\def\@shorttitleaux{}
\def\@titleaux{}
\def\@subtitleaux{}
\def\@author{}
\def\@copyrightdate{}
\def\@privateaddress{}

\def\@dedication{}
\def\@famouscite{}

\def\@prefacefile{}
\def\@ackfile{}
\def\@resumenfile{}
\def\@abstractfile{}
\def\@auxkeywords{}
\def\@auxpalabrasclave{}
\def\@auxcoverdata{}

\def\advisor#1{\def\@advisor{#1}}
\def\coadvisor#1{\def\@coadvisor{#1}}
\def\speaker#1{\def\@speaker{#1}}
\def\levelin#1{\def\@levelin{#1}}
\def\faculty#1{\def\@faculty{#1}}
\renewcommand{\title}[2][]{\if&#1&\def\@shorttitleaux{#2}\else\def\@shorttitleaux{#1}\fi \def\@titleaux{#2}}
\def\subtitle#1{\@subtitlebooltrue \def\@subtitleaux{#1}}
\def\author#1{\def\@author{#1}}
\def\copyrightdate#1{\def\@copyrightdate{#1}}
\def\privateaddress#1{\def\@privateaddress{#1}}

\def\dedication#1{\def\@dedication{#1}}
\def\famouscite#1{\def\@famouscite{#1}}

\def\prefacefile#1{\def\@prefacefile{#1}}
\def\ackfile#1{\def\@ackfile{#1}}
\def\resumenfile#1{\def\@resumenfile{#1}}
\def\abstractfile#1{\def\@abstractfile{#1}}

\def\keywords#1{\def\@auxkeywords{#1}}
\def\palabrasclave#1{\def\@auxpalabrasclave{#1}}

\def\coverdata#1{\def\@auxcoverdata{#1}}

\def\codesdir#1{\def\@auxcodesdir{#1}}
\def\datadir#1{\pgfplotsset{table/search path={#1},}}
\def\graphicsdir#1{\def\@auxgraphicsdir{#1}}
\def\logosdir#1{\@logosdirbooltrue \def\@auxlogosdir{#1}}

\def\facultylogo#1{\def\@facultylogo{#1}}
\def\facultylogowide#1{\def\@facultylogowide{#1}}

\def\listinterlined#1{\def\@listinterlined{#1}}
\listinterlined{0.1\myem}

\renewcommand{\baselinestretch}{1.3}
\setlength{\parskip}{0.7\baselineskip}

\logosdir{.}
\codesdir{.}
\datadir{.}
\graphicsdir{.}

\facultylogowide{}
\facultylogo{}
\faculty{}

\if@epsbool \facultylogo{logoEPS} \facultylogowide{0.16\textwidth} \faculty{Escuela Politécnica Superior}\fi
\if@cienciasbool \facultylogo{logoCiencias} \facultylogowide{0.32\textwidth} \faculty{Facultad de Ciencias} \fi
\if@medicinabool \facultylogo{logoMedicina} \facultylogowide{0.32\textwidth} \faculty{Facultad de Medicina} \fi
\if@enfermeriabool \facultylogo{logoMedicina} \facultylogowide{0.32\textwidth} \faculty{Escuela de Enfermería} \fi
\if@fisioterapiabool \facultylogo{logoMedicina} \facultylogowide{0.32\textwidth} \faculty{Escuela de Fisioterapia} \fi
\if@psicologiabool \facultylogo{logoPsicologia} \facultylogowide{0.32\textwidth} \faculty{Facultad de Psicología} \fi
\if@filosofiabool \facultylogo{logoFilosofia} \facultylogowide{0.16\textwidth} \faculty{Facultad de Filosofia y Letras} \fi
\if@profesoradobool \facultylogo{logoProfesorado} \facultylogowide{0.32\textwidth} \faculty{Facultad de Filosofia y Letras} \fi
\if@derechobool \facultylogo{logoDerecho} \facultylogowide{0.32\textwidth} \faculty{Facultad de Derecho} \fi
\if@economicasbool \facultylogo{logoEconomicas} \facultylogowide{0.36\textwidth} \faculty{Facultad de Ciencias Económicas y Empresariales} \fi


\def\setnames{
	\if@languagespa
		\def\@ListsChapter{Listas}
		\def\glossaryname{Definiciones}
		\def\listacronymname{Acrónimos}
		\def\@auxvarcode{Código}
		\def\@auxvarcodeindex{\addtocounter{section}{1}Lista de códigos}
		\def\@auxvartextbox{Cuadro}
		\def\@auxvartextboxindex{\addtocounter{section}{1}Lista de cuadros}
		\def\contentsname{Índice}
		\def\bibname{Bibliografía}
		\def\appendixname{Apéndices}
		\def\listfigurename{\addtocounter{section}{1}Lista de figuras}
		\def\listequationname{\addtocounter{section}{1}Lista de ecuaciones}
		\def\figurename{Figura}
		\def\listtablename{\addtocounter{section}{1}Lista de tablas}
		\def\tablename{Tabla}
		\def\@auxvaralgorithm{Algoritmo}
		\def\@auxvaralgorithmindex{\addtocounter{section}{1}Lista de algoritmos}
		\def\indexname{Índice terminológico}
		\def\glosario{Glosario}
		\renewcommand*{\acronymname}{Acrónimos}
	\else
		\def\@ListsChapter{Lists}
		\def\glossaryname{Terminology}
		\def\listacronymname{Acronyms}
		\def\@auxvarcode{Code}
		\def\@auxvarcodeindex{\addtocounter{section}{1}List of codes}
		\def\@auxvartextbox{Frame}
		\def\@auxvartextboxindex{\addtocounter{section}{1}List of text boxes}
		\def\contentsname{Table of Contents}
		\def\bibname{Bibliography}
		\def\appendixname{Appendices}
		\def\listfigurename{\addtocounter{section}{1}List of figures}
		\def\listequationname{\addtocounter{section}{1}List of equations}
		\def\figurename{Figure}
		\def\listtablename{\addtocounter{section}{1}List of tables}
		\def\tablename{Table}
		\def\@auxvaralgorithm{Algorithm}
		\def\@auxvaralgorithmindex{\addtocounter{section}{1}List of algorithms}
		\def\indexname{Index}
		\def\glosario{Glossary}
		\renewcommand*{\acronymname}{Acronyms}
	\fi
}

\newcommand{\pdfmetavalues}[4]
{
	\pdfinfo{
		/Title  (#2)
		/Author (#1)
		/Creator (#1)
		/CreationDate (D:\pdfdate)
		/Subject (#3)
		/Keywords (#4)
	}
}

\if@printmodebool
	\hypersetup{
		pdfnewwindow=true,
		unicode=false,          % non-Latin characters in Acrobat’s bookmarks
		pdftoolbar=true,        % show Acrobat’s toolbar?
		pdfmenubar=true,        % show Acrobat’s menu?
		pdffitwindow=false,     % window fit to page when opened
		pdfstartview={FitH},    % fits the width of the page to the window
		pdfproducer={Eloy Anguiano Rey}, % producer of the document
		pdfnewwindow=true,      % links in new PDF window
		colorlinks=true,       	% false: boxed links; true: colored links
		anchorcolor=black,
	  linkcolor=black, 				% color of internal links (change box color with linkbordercolor)
	  citecolor=black,  			% color of links to bibliography
	  filecolor=black, 				% color of file links
	  urlcolor=black,  				% color of external links
		hidelinks,          		% Links not showed
		pdfhighlight=/P,
		breaklinks
	}
\else
	\hypersetup{
		pdfnewwindow=true,
	  unicode=false,          % non-Latin characters in Acrobat’s bookmarks
	  pdftoolbar=true,        % show Acrobat’s toolbar?
	  pdfmenubar=true,        % show Acrobat’s menu?
	  pdffitwindow=false,     % window fit to page when opened
	  pdfstartview={FitH},    % fits the width of the page to the window
	  pdfproducer={Eloy Anguiano Rey}, % producer of the document
	  pdfnewwindow=true,      % links in new PDF window
	  colorlinks=true,      	% false: boxed links; true: colored links
		anchorcolor=dmaincolor,
	  linkcolor=dmaincolor, 	% color of internal links (change box color with linkbordercolor)
	  citecolor=dmaincolor,  	% color of links to bibliography
	  filecolor=dmaincolor, 	% color of file links
	  urlcolor=dmaincolor,  	% color of external links
		pdfhighlight=/P,
		breaklinks
		}
	\fi

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                      Fonts                       %%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


\if@nineptbool
	\setlength{\paperheight}{229mm}  \setlength{\paperwidth}{162mm}
	\def\coverfont 		{\fontsize{37}{51}		\usefont{T1}{pxss}{m}{n}	\selectfont}
	\def\numpartfont 		{\fontsize{61}{77}		\usefont{T1}{pxss}{b}{sc}	\selectfont}
	\def\numchapfont 		{\fontsize{75}{80}		\usefont{T1}{pxss}{m}{n}	\selectfont}
	\def\txtpartfont 		{\fontsize{35}{44}		\usefont{T1}{pxss}{b}{sc}	\selectfont}
	\def\txtchapfont		{\fontsize{25}{28}		\usefont{T1}{pxss}{b}{sc}	\selectfont}
	\def\txtuamfont 		{\fontsize{21}{24}		\usefont{T1}{pxss}{b}{sc}	\selectfont}
	\def\txtepsfont 		{\fontsize{19}{21}		\usefont{T1}{pxss}{b}{sc}	\selectfont}
	\def\txttitletfgfont 	{\fontsize{17}{20}		\usefont{T1}{pxss}{b}{sc}	\selectfont}
	\def\txttitlefont 		{\fontsize{14}{18}	\usefont{T1}{pxss}{b}{n}	\selectfont}
	\def\txtfont 			{\fontsize{8}{10}	\usefont{T1}{txss}{m}{n}	\selectfont}
	\def\txtboxfont 		{\fontsize{8}{10}	\usefont{T1}{txss}{m}{sl}	\selectfont}
	\def\txtcopyrightfont	{\fontsize{8}{10}		\usefont{T1}{cmr}{m}{n}		\selectfont}
	\def\codefont			{\fontsize{8}{10} 		\usefont{T1}{cmr}{m}{n}		\selectfont}
\fi
\if@tenptbool
  \setlength{\paperheight}{250mm}  \setlength{\paperwidth}{176mm}
	\def\coverfont 		{\fontsize{43}{57}		\usefont{T1}{pxss}{m}{n}	\selectfont}
	\def\numpartfont 		{\fontsize{67}{83}		\usefont{T1}{pxss}{b}{sc}	\selectfont}
	\def\numchapfont 		{\fontsize{83}{88}		\usefont{T1}{pxss}{m}{n}	\selectfont}
	\def\txtpartfont 		{\fontsize{37}{46}		\usefont{T1}{pxss}{b}{sc}	\selectfont}
	\def\txtchapfont		{\fontsize{29}{32}		\usefont{T1}{pxss}{b}{sc}	\selectfont}
	\def\txtuamfont 		{\fontsize{25}{28}		\usefont{T1}{pxss}{b}{sc}	\selectfont}
	\def\txtepsfont 		{\fontsize{23}{25}		\usefont{T1}{pxss}{b}{sc}	\selectfont}
	\def\txttitletfgfont 	{\fontsize{21}{24}		\usefont{T1}{pxss}{b}{sc}	\selectfont}
	\def\txttitlefont 		{\fontsize{17.5}{21}	\usefont{T1}{pxss}{b}{n}	\selectfont}
	\def\txtfont 			{\fontsize{10}{13.3}	\usefont{T1}{txss}{m}{n}	\selectfont}
	\def\txtboxfont 		{\fontsize{10}{13.3}	\usefont{T1}{txss}{m}{sl}	\selectfont}
	\def\txtcopyrightfont	{\fontsize{10}{15}		\usefont{T1}{cmr}{m}{n}		\selectfont}
	\def\codefont			{\fontsize{10}{12} 		\usefont{T1}{cmr}{m}{n}		\selectfont}
\fi
\if@elevenptbool
	\setlength{\paperheight}{297mm}  \setlength{\paperwidth}{210mm}
	\def\wwwfont				{\fontsize{25}{30} \usefont{T1}{pxr}{b}{n}\selectfont}
	\def\coverfont 			{\fontsize{47}{62}		\usefont{T1}{pxss}{m}{n}	\selectfont}
	\def\numpartfont		{\fontsize{73}{89} 		\usefont{T1}{pxss}{b}{sc}	\selectfont}
	\def\numchapfont		{\fontsize{91}{96}		\usefont{T1}{pxss}{m}{n}	\selectfont}
	\def\txtpartfont		{\fontsize{39}{50} 		\usefont{T1}{pxss}{b}{sc}	\selectfont}
	\def\txtchapfont		{\fontsize{32}{35} 		\usefont{T1}{pxss}{b}{sc}	\selectfont}
	\def\txtuamfont			{\fontsize{27}{30}		\usefont{T1}{pxss}{b}{sc}	\selectfont}
	\def\txtepsfont			{\fontsize{24.5}{27} 	\usefont{T1}{pxss}{b}{sc}	\selectfont}
	\def\txttitletfgfont	{\fontsize{23}{26} 		\usefont{T1}{pxss}{b}{sc}	\selectfont}
	\def\txttitlefont 		{\fontsize{19}{23} 		\usefont{T1}{pxss}{b}{n}	\selectfont}
	\def\txtfont 			{\fontsize{11}{14} 		\usefont{T1}{txss}{m}{n}	\selectfont}
	\def\txtboxfont 		{\fontsize{11}{14} 		\usefont{T1}{txss}{m}{sl}	\selectfont}
	\def\txtcopyrightfont 	{\fontsize{11}{16} 		\usefont{T1}{cmr}{m}{n}		\selectfont}
	\def\codefont 			{\fontsize{11}{13}		\usefont{T1}{cmr}{m}{n}		\selectfont}
\fi

\def\txtsecfont 		{\txtfont\bfseries\LARGE}
\def\txtsubsecfont 		{\txtfont\bfseries\Large}
\def\txtsubsubsecfont 	{\txtfont\bfseries\large}
\def\txtdoxyfont 		{\txtfont\bfseries}
\def\txtparfont 		{\txtfont\bfseries}
\def\txtsubparfont 		{\txtfont\bfseries}
\def\txttitlefont 		{\txtfont\bfseries\Large}
\def\txtfontbold 		{\txtfont\bfseries}
\def\txtfontbbold		{\txtfont\bfseries\large}
\def\algonumfont 		{\txtfont\bfseries\footnotesize}

\def\normalsize			{\txtfont}
\def\normalfont			{\txtfont}

\pgfplotsset{compat=1.13}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%                    DECORATIONS                       %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\renewcommand{\headrulewidth}{1\mypt}
\renewcommand{\footrulewidth}{1\mypt}

\def\headrule
{
	{\color{headfootcolor}
	\if@fancyplain\let\headrulewidth\plainheadrulewidth\fi
	\hrule\@height\headrulewidth\@width\headwidth \vskip-\headrulewidth}
}

\def\footrule
{
	{\color{headfootcolor}
	\if@fancyplain\let\footrulewidth\plainfootrulewidth\fi
	\vskip-\footruleskip\vskip-\footrulewidth
	\hrule\@width\headwidth\@height\footrulewidth\vskip\footruleskip}
}

\fancypagestyle{firstpage}
{
	\if@firstchappagnumbool
		\fancyhf{}
		\fancyfoot[C]{\color{headfootcolor}\thepage}
		\fancyhead[C]{}
		\renewcommand{\headrulewidth}{0\mypt}
		\renewcommand{\footrulewidth}{0\mypt}
	\else
		\fancyhf{}
		\renewcommand{\headrulewidth}{0\mypt}
		\renewcommand{\footrulewidth}{0\mypt}
	\fi
}

\fancypagestyle{prefacepage}
{
	\fancyhf{}
	\fancyfoot[C]{\color{headfootcolor}\thepage}
	\fancyhead[C]{}
	\renewcommand{\headrulewidth}{0\mypt}
	\renewcommand{\footrulewidth}{0\mypt}
}

\fancypagestyle{normalpage}
{
	\fancyhf{}
	\fancyhead[RO]{\color{headfootcolor}\scshape \nouppercase\rightmark}
	\fancyhead[LE]{\color{headfootcolor}\scshape \nouppercase\leftmark}
	\fancyfoot[LE,RO]{\color{headfootcolor}\thepage}
	\fancyfoot[LO]{\color{headfootcolor}\@author}
	\fancyfoot[RE]{\color{headfootcolor}\@shorttitleaux}
	\renewcommand{\headrulewidth}{1\mypt}
	\renewcommand{\footrulewidth}{1\mypt}
}

\fancypagestyle{indexst}{%
	\renewcommand{\headrulewidth}{0pt}
	\renewcommand{\footrulewidth}{0pt}
	\fancyhf{}
	\fancyfoot[C]{\thepage}
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%                       COLORS                         %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\definecolor{uamgray}{HTML}{78797D}
\definecolor{luamgray}{HTML}{9C9DA0}
\definecolor{vluamgray}{HTML}{C0C1C5}

\def\complementaries#1
{
	\colorlet{#1one}{#1}
	\colorlet{#1two}[HTML]{#1>wheel,2,4}
	\colorlet{#1three}[HTML]{#1>wheel,3,4}
	\colorlet{#1four}[HTML]{#1>wheel,1,4}
	\colorlet{#1five}[HTML]{#1>wheel,7,8}
	\colorlet{#1six}[HTML]{#1>wheel,5,8}
	\colorlet{#1seven}[HTML]{#1>wheel,1,8}
	\colorlet{#1eight}[HTML]{#1>wheel,3,8}
}

\def\definemycolor#1#2#3
{
	\colorlet{@co#1#2color}{#2color!#3}
	\definecolor{#1#2based}{named}{@co#1#2color}
	\complementaries{#1#2based}
}

\def\definemycolorset#1#2
{
	\definemycolor{#1}{uam}{#2}
	\definemycolor{#1}{ciencias}{#2}
	\definemycolor{#1}{economicas}{#2}
	\definemycolor{#1}{derecho}{#2}
	\definemycolor{#1}{filosofia}{#2}
	\definemycolor{#1}{profesorado}{#2}
	\definemycolor{#1}{medicina}{#2}
	\definemycolor{#1}{psicologia}{#2}
	\definemycolor{#1}{eps}{#2}
	\definemycolor{#1}{enfermeria}{#2}
	\definemycolor{#1}{fisioterapia}{#2}
	\definemycolor{#1}{blue}{#2}
	\definemycolor{#1}{green}{#2}
	\definemycolor{#1}{red}{#2}
	\definemycolor{#1}{magenta}{#2}
	\definemycolor{#1}{yellow}{#2}
	\definemycolor{#1}{cyan}{#2}
	\definemycolor{#1}{orange}{#2}
	\definemycolor{#1}{black}{#2}
	\definemycolor{#1}{gray}{#2}
}

\definecolor{draftcolor}{HTML}{FFE5E5}

\definecolorset{HTML}{}{color}{uam,00A65C;ciencias,1C5D91;economicas,D67C34;derecho,C1495D;filosofia,5DA4EB;profesorado,007674;medicina,DB9434;psicologia,A981D4;eps,9A7249;enfermeria,A6ACB5;fisioterapia,32BEC0;blue,8080FF;green,80FF80;red,FF8080;magenta,FF80FF;yellow,FFFF80;cyan,80FFFF;orange,FF8800;black,000000;gray,808080}

\definemycolorset{ud}{160}
\definemycolorset{vd}{140}
\definemycolorset{d}{120}
\definemycolorset{}{100}
\definemycolorset{l}{80}
\definemycolorset{vl}{60}
\definemycolorset{ul}{40}
\definemycolorset{bg}{20}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Working with colors
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


\def\colorbased#1#2#3#4#5#6{
	\definecolor{descriptioncolor}{named}{#1}
	\definecolor{headfootcolor}{named}{#1}
	\definecolor{maincolor}{named}{#1}
	\definecolor{textboxfgcolor}{named}{#1}
	\definecolor{codefgcolor}{named}{#1}
	\definecolor{equationfgcolor}{named}{#1}
	\definecolor{codebgcolor}{named}{#2}
	\definecolor{equationbgcolor}{named}{#2}
	\definecolor{textboxbgcolor}{named}{#2}
	\definecolor{commentcolor}{named}{#3}
	\definecolor{dmaincolor}{named}{#3}
	\definecolor{textcolor}{named}{black}

	\definecolor{complementaryone}{named}{#4one}
	\definecolor{complementarytwo}{named}{#4two}
	\definecolor{complementarythree}{named}{#4three}
	\definecolor{complementaryfour}{named}{#4four}
	\definecolor{complementaryfive}{named}{#4five}
	\definecolor{complementarysix}{named}{#4six}
	\definecolor{complementaryseven}{named}{#4seven}
	\definecolor{complementaryeight}{named}{#4eight}

	\definecolor{complementarylightone}{named}{#5one}
	\definecolor{complementarylighttwo}{named}{#5two}
	\definecolor{complementarylightthree}{named}{#5three}
	\definecolor{complementarylightfour}{named}{#5four}
	\definecolor{complementarylightfive}{named}{#5five}
	\definecolor{complementarylightsix}{named}{#5six}
	\definecolor{complementarylightseven}{named}{#5seven}
	\definecolor{complementarylighteight}{named}{#5eight}

	\definecolor{complementarydarkone}{named}{#6one}
	\definecolor{complementarydarktwo}{named}{#6two}
	\definecolor{complementarydarkthree}{named}{#6three}
	\definecolor{complementarydarkfour}{named}{#6four}
	\definecolor{complementarydarkfive}{named}{#6five}
	\definecolor{complementarydarksix}{named}{#6six}
	\definecolor{complementarydarkseven}{named}{#6seven}
	\definecolor{complementarydarkeight}{named}{#6eight}

	\typeout{Colors defined}
}


\if@uambool \colorbased{uambased}{bguambased}{uduambased}{uambased}{vluambased}{vduambased}	\fi
\if@cienciasbool \colorbased{cienciasbased}{bgcienciasbased}{udcienciasbased}{cienciasbased}{vlcienciasbased}{vdcienciasbased}	\fi
\if@economicasbool \colorbased{economicasbased}{bgeconomicasbased}{udeconomicasbased}{economicasbased}{vleconomicasbased}{vdeconomicasbased}	\fi
\if@derechobool \colorbased{derechobased}{bgderechobased}{udderechobased}{derechobased}{vlderechobased}{vdderechobased}	\fi
\if@filosofiabool \colorbased{filosofiabased}{bgfilosofiabased}{udfilosofiabased}{filosofiabased}{vlfilosofiabased}{vdfilosofiabased}	\fi
\if@profesoradobool \colorbased{profesoradobased}{bgprofesoradobased}{udprofesoradobased}{profesoradobased}{vlprofesoradobased}{vdprofesoradobased} \fi
\if@medicinabool \colorbased{medicinabased}{bgmedicinabased}{udmedicinabased}{medicinabased}{vlmedicinabased}{vdmedicinabased}	\fi
\if@psicologiabool \colorbased{psicologiabased}{bgpsicologiabased}{udpsicologiabased}{psicologiabased}{vlpsicologiabased}{vdpsicologiabased}	\fi
\if@epsbool \colorbased{epsbased}{bgepsbased}{udepsbased}{epsbased}{vlepsbased}{vdepsbased}	\fi
\if@enfermeriabool \colorbased{enfermeriabased}{bgenfermeriabased}{udenfermeriabased}{medicinabased}{vlmedicinabased}{vdmedicinabased}	\fi
\if@fisioterapiabool \colorbased{fisioterapiabased}{bgfisioterapiabased}{udfisioterapiabased}{fisioterapiabased}{vlfisioterapiabased}{vdfisioterapiabased}	\fi
\if@bluecolorbool \colorbased{bluebased}{bgbluebased}{udbluebased}{bluebased}{vlbluebased}{vdbluebased}	\fi
\if@greencolorbool \colorbased{greebased}{bggreebased}{udgreebased}{greebased}{vlgreebased}{vdgreebased}	\fi
\if@magentacolorbool \colorbased{magentabased}{bgmagentabased}{udmagentabased}{magentabased}{vlmagentabased}{vdmagentabased}	\fi
\if@yellowcolorbool \colorbased{yellowbased}{bgyellowbased}{udyellowbased}{yellowbased}{vlyellowbased}{vdyellowbased}	\fi
\if@cyancolorbool \colorbased{cyanbased}{bgcyanbased}{udcyanbased}{cyanbased}{vlcyanbased}{vdcyanbased}	\fi
\if@orangecolorbool \colorbased{orangebased}{bgorangebased}{udorangebased}{orangebased}{vlorangebased}{vdorangebased}	\fi
\if@blackcolorbool \colorbased{blackbased}{bgblackbased}{udblackbased}{blackbased}{vlblackbased}{vdblackbased}	\fi
\if@graycolorbool \colorbased{graybased}{bggraybased}{udgraybased}{graybased}{vlgraybased}{vdgraybased}	\fi

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%                       LENGTHS                        %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newlength{\exposa}
\newlength{\exposb}
\newlength{\exposc}

\setlength\overfullrule{0\mypt}

\setlength{\textwidth}{0.79\paperwidth}

\setlength{\textheight}{0.82\paperheight}
\setlength{\footskip}{0.056\paperheight}
\setlength{\headheight}{0.053\paperheight}
\setlength{\headsep}{0.046\paperheight}

\setlength{\topmargin}{-0.013\paperheight}
\addtolength{\topmargin}{-1in}
\topskip=0\mypt

\hoffset=0in
\voffset=0in

\parskip=0.8\myem
\parindent=4\myex

\renewcommand{\@dotsep}{2}

\renewcommand{\subfigcapskip}{0.5\myem}
\renewcommand{\subfigbottomskip}{0.3\myem}

\widowpenalty=30
\clubpenalty=30

\abovedisplayskip=-2.8\myex
\abovedisplayshortskip=-2.8\myex
\belowdisplayskip=-2.8\myex
\belowdisplayshortskip=-2.8\myex


\if@printmodebool
	\setlength{\oddsidemargin}{0.15\paperwidth}
	\addtolength{\oddsidemargin}{-1in}
	\setlength{\evensidemargin}{0.06\paperwidth}
	\addtolength{\evensidemargin}{-1in}
\else
	\setlength{\oddsidemargin}{0.105\paperwidth}
	\addtolength{\oddsidemargin}{-1in}
	\setlength{\evensidemargin}{0.105\paperwidth}
	\addtolength{\evensidemargin}{-1in}
\fi


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Table of contents look up control
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\renewcommand{\cftdotsep}{2}
\renewcommand{\cftbeforepartskip}{0.4\myem}
\renewcommand{\cftbeforechapskip}{-.3\myem}
\renewcommand{\cftbeforesecskip}{-.7\myem}
\renewcommand{\cftbeforesubsecskip}{-.7\myem}
\renewcommand{\cftbeforesubsubsecskip}{-.7\myem}
\renewcommand{\cftchapindent}{2\myex}
\renewcommand{\cftsecindent}{4\myex}
\renewcommand{\cftsubsecindent}{6\myex}
\renewcommand{\cftsubsubsecindent}{8\myex}
\renewcommand{\cftpartfont}{\txtfontbbold}
\renewcommand{\cftchapfont}{\txtfontbold}
\renewcommand{\cftsecfont}{\txtfont}
\renewcommand{\cftsubsecfont}{\txtfont}
\renewcommand{\cftsubsubsecfont}{\txtfont}
\renewcommand{\cftfigfont}{\txtfont}
\renewcommand{\cfttabfont}{\txtfont}
\renewcommand{\cftfignumwidth}{5.5\myex}
\renewcommand{\cfttabnumwidth}{5.5\myex}
\cftsetpnumwidth{6\myex}

\renewcommand*\l@figure{\@dottedtocline{1}{4\myex}{2.8\myem}}
\let\l@table\l@figure


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%                        STRUCT                        %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newlength{\chapterheight}
\setlength{\chapterheight}{0.24\paperheight}

\def\@resetpages{
	\if@gotfirstpage \else
		\renewcommand{\thepage}{\arabic{page}}
		\setcounter{page}{1}
		\setcounter{chapter}{0}
		\setcounter{part}{0}
		\@gotfirstpagetrue
	\fi
}


\def\cleardoublepage{
	\clearpage
	\ifodd
		\c@page
	\else
		\vspace*{\fill}
		\thispagestyle{empty}
		\newpage
	\fi
}

\def\clearsdoublepage{
	\clearpage
	\ifodd
		\c@page
	\else
		\vspace*{\fill}
		\newpage
	\fi
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Redefinition of appendix
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newcounter{appendixc}
\setcounter{appendixc}{0}

\let\oldappendix\appendix

\renewcommand\appendix
{
	\@appendixbooltrue
	\thesisbibliography
	\printglossaries
	\part{\appendixname}
	\oldappendix
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Redefinition of part
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\def\@part[#1]#2{
	\thispagestyle{empty}
	\@resetpages
	\ifnum \c@secnumdepth >-2\relax
		\refstepcounter{part}
		\addcontentsline{toc}{part}{#1}
	\else
		\addcontentsline{toc}{part}{#1}
	\fi
	\markboth{}{}

	{\centering
		\interlinepenalty \@M
		\normalfont
		{\color{maincolor} \txtpartfont \scshape #2 \par}
	}
	\@endpart
}

\def\@spart#1
{
	\thispagestyle{empty}
	\@resetpages
	\if@rstnum
		\ifx\thenumpageadd\empty
			\@gotfirstpagefalse
			\@resetpages
		\else
			\edef\aux@pag{\thenumpageadd}
			\renewcommand{\thepage}{\aux@pag.\arabic{page}}
			\setcounter{page}{1}
		\fi
		\@rstnumfalse
	\fi
	\ifnum \c@secnumdepth >-2\relax
		\if@thesispartbool
			\addcontentsline{toc}{part}{#1}
			\@thesispartboolfalse
		\fi
	\else
		\if@thesispartbool
			\addcontentsline{toc}{part}{#1}
			\@thesispartboolfalse
		\fi
	\fi
	\markboth{}{}
	{\centering
		\interlinepenalty \@M
		{\color{maincolor} \txtpartfont \scshape #1 \par}
	}
	\@endpart
}

\def\@endpart{
	\vfil\newpage
	\if@twoside
		\if@openright
			\null
			\thispagestyle{empty}
			\newpage
		\fi
	\fi
	\if@tempswa
		\twocolumn
	\fi
	\@ifnextchar\bgroup{\input}{\empty}
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Chapter control
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\renewcommand\chapter{
	\global\@topnum\z@
	\secdef\@newchapter\@newschapter
}

\newcommand{\@newchapter}[2][]
{
	\@preambletextfalse
	\cleardoublepage
	\@resetpages
	\if@rstnum
		\ifx\thenumpageadd\empty
			\@gotfirstpagefalse
			\@resetpages
		\else
			\edef\aux@pag{\thenumpageadd}
			\renewcommand{\thepage}{\aux@pag.\arabic{page}}
			\setcounter{page}{1}
		\fi
		\@rstnumfalse
	\fi
	\ifx&#1& \@chapter{#2} \else \@chapter[#1]{#2} \fi
	\addtocontents{loa}{\protect\addvspace{10\p@}}
	\addtocontents{loe}{\protect\addvspace{10\p@}}
	\addtocontents{lol}{\protect\addvspace{10\p@}}
	\addtocontents{ltb}{\protect\addvspace{10\p@}}
	\thispagestyle{firstpage}
	\pagestyle{normalpage}
	\@ifnextchar\bgroup{\input}{\empty}
}

\newcommand{\@newschapter}[2][]
{
	\cleardoublepage
	\ifx&#1& \@schapter{#2} \else \@schapter[#1]{#2} \fi
	\addtocontents{loa}{\protect\addvspace{10\p@}}
	\addtocontents{loe}{\protect\addvspace{10\p@}}
	\addtocontents{lol}{\protect\addvspace{10\p@}}
	\addtocontents{ltb}{\protect\addvspace{10\p@}}
	\if@preambletext
		\pagestyle{prefacepage}
	\else
		\thispagestyle{firstpage}
		\pagestyle{normalpage}
	\fi

	\@ifnextchar\bgroup{\input}{\empty}
}

\newcommand{\@newschapterlistof}[2][]
{
	\ifx&#1& \@schapter{#2} \else \@schapter[#1]{#2} \fi
	\if@preambletext
		\pagestyle{prefacepage}
	\else
		\thispagestyle{firstpage}
		\pagestyle{normalpage}
	\fi

	\@ifnextchar\bgroup{\input}{\empty}
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Chapter heading
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\def\thickhrulefill{\color{maincolor} \leavevmode \leaders \hrule height 0.35\myex \hfill \kern \z@}
\def\chapvrule{ \vrule height 15\myex width 0.35\myex }

\def\@makechapterhead#1{
	\markboth{#1}{}
	\setlength{\parskip}{0\myex plus 0\myex minus 0\myex}
	\vspace*{10\p@}
	{\parindent \z@ \reset@font
		\vspace*{-0.067\paperheight}
		\vbox to \chapterheight {
			\color{maincolor}
			{\numchapfont \begin{flushright} \chapvrule \hspace*{0.02\myex} \thechapter \end{flushright}}
			\vspace*{-2.4\myem}
			\begin{flushleft}
				\txtchapfont
				#1
				\vspace*{-2\myem}
			\end{flushleft}
			\thickhrulefill
			\vfill
			}
		\par
	}
	\parskip=0.8\myem
}

\def\@makeschapterhead#1{
	\markboth{#1}{}
	\setlength{\parskip}{1.1\myex plus 0\myex minus 0\myex}
	\vspace*{10\p@}
	{\parindent \z@ \reset@font
		{\color{maincolor}
		\vspace*{-3\myem} {\begin{flushleft}{\txtchapfont #1}\end{flushleft}}\vspace*{-2.2\myem}\thickhrulefill}
		\vspace*{4\myem}
		\par
	}
	\parskip=0.8\myem
	\setcounter{section}{\z@}
}



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Section, subsection ... headings
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\renewcommand\section[2][]
{
	\if&#1& \mysection{#2} \else \mysection[#1]{#2} \fi
	\@ifnextchar\bgroup{\input}{\empty}
}

\renewcommand\subsection[2][]
{
	\if&#1& \mysubsection{#2} \else \mysubsection[#1]{#2} \fi
	\@ifnextchar\bgroup{\input}{\empty}
}

\renewcommand\subsubsection[2][]
{
	\if&#1& \mysubsubsection{#2} \else \mysubsubsection[#1]{#2} \fi
	\@ifnextchar\bgroup{\input}{\empty}
}

\renewcommand\paragraph[2][]
{
	\if&#1& \myparagraph{#2} \else \myparagraph[#1]{#2} \fi \par
	\@ifnextchar\bgroup{\input}{\empty}
}

\newcommand\paragraphs[2][]
{
	\if&#1& \myparagraphs{#2} \else \myparagraphs[#1]{#2} \fi \par
	\@ifnextchar\bgroup{\input}{\empty}
}

\renewcommand\subparagraph[2][]
{
	\if&#1& \mysubparagraph{#2} \else \mysubparagraph[#1]{#2} \fi \par
	\@ifnextchar\bgroup{\input}{\empty}
}

\newcommand\mysection{\@startsection{section}{1}{\z@}{-2\myem \@plus -.5\myem \@minus -.2\myem}{1\myem \@plus .2\myem \@minus .2\myem}{\color{maincolor}\txtsecfont\raggedright}}
\newcommand\mysubsection{\@startsection{subsection}{2}{\z@}{-1.6\myem \@plus -.4\myem \@minus -.15\myem}{0.8\myem \@plus .15\myem \@minus .15\myem}{\color{maincolor}\txtsubsecfont}}
\newcommand\mysubsubsection{\@startsection{subsubsection}{3}{\z@}{-1.2\myem \@plus -.3\myem \@minus -.1\myem}{0.6\myem \@plus .1\myem \@minus .1\myem}{\color{maincolor}\txtsubsubsecfont}}
\newcommand\myparagraphs{\@startsection{paragraph}{4}{\z@}{-2\myem \@plus -.5\myem \@minus -.2\myem}{1\myem \@plus .2\myem \@minus .2\myem}{\color{maincolor}\txtsecfont\raggedright}}
\newcommand\myparagraph{\@startsection{paragraph}{4}{\z@}{-0.8\myem \@plus -.2\myem \@minus -.08\myem}{0.6\myem \@plus .08\myem \@minus .08\myem}{\color{maincolor}\txtparfont}}
\newcommand\mysubparagraph{\@startsection{subparagraph}{5}{\parindent}{-0.4\myem \@plus -.15\myem \@minus -.06\myem}{0.4\myem \@plus .06\myem \@minus .06\myem}{\color{maincolor}\txtsubparfont}}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%                        FIGURES                       %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Figure float structure
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\renewenvironment{figure}[3][]
{
	\def\my@auxcaptiontext{#3}
	\ifx&#1& \def\my@auxcaptiontextshort{} \else \def\my@auxcaptiontextshort{#1} \fi
	\ifx&#2& \def\my@auxcaptionlabel{} \else \def\my@auxcaptionlabel{#2} \fi
	\@float{figure}[htbp]
		\begin{center}
}
{
		\end{center}
		\caption[\my@auxcaptiontextshort]{\label{\my@auxcaptionlabel}\my@auxcaptiontext}
	\end@float
}

\renewenvironment{figure*}[3][]
{
	\@dbfloat{figure}[htbp]
		\caption[#1]{#3}
		\label{#2}
		\begin{center}
}
{
		\end{center}
	\end@dbfloat
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% image and imagec macros
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newcommand{\logopgfimage}[2][]
{
	\if&#1& \IfFileExists{\@auxlogosdir/#2}{\pgfimage{\@auxlogosdir/#2}}{\pgfimage{#2}}
	\else \IfFileExists{\@auxlogosdir/#2}{\pgfimage[#1]{\@auxlogosdir/#2}}{\pgfimage[#1]{#2}}
	\fi
}


\def\@mypgfimage#1#2#3
{
	\ifx&#1&
		\ifx&#2&
			\typeout{Figure #3 without any size data using 0.9*textwidth}
			\pgfimage[width=0.9\textwidth]{\@auxgraphicsdir/#3}
		\else
			\typeout{Figure #3 with height data}
			\pgfimage[height=#2]{\@auxgraphicsdir/#3}
		\fi
	\else
		\ifx&#2&
			\typeout{Figure #3 with width data}
			\pgfimage[width=#1]{\@auxgraphicsdir/#3}
		\else
			\typeout{Figure #3 with height and width data}
			\pgfimage[width=#1,height=#2]{\@auxgraphicsdir/#3}
		\fi
	\fi
}

\let\oldsubfigure\subfigure

\renewcommand{\subfigure}[3][]
{
	\ifx&#2& \oldsubfigure[lof][]
	{
		\ifx&#1& \else \label{#1} \fi
		#3
	}
	\else \oldsubfigure[lof][#2]
	{
		\ifx&#1& \else \label{#1} \fi
		#3
	}
	\fi
}


\def\image#1#2#3{\@mypgfimage{#1}{#2}{#3}}

\newcommand{\imageIL}[2]
{
	\begin{wrapfigure}{l}{#1}
		\scalebox{0.95}
		{
			\pgfimage[width=#1]{\@auxgraphicsdir/#2}
		}
	\end{wrapfigure}
}



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%                      TEXT BOXES                      %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Text box float structure
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\floatname{textboxb}{\@auxvartextbox}
\floatstyle{plain}
\newfloat{textboxb}{htbp}{ltb}[chapter]

\newsavebox{\@temptextboxa}

\newenvironment{textbox}[3][]
{
	\renewcommand{\abovecaptionskip}{0\myem}
	\begin{textboxb}
		\ifx&#1&
			\caption[#1]{\label{#2}#3}
		\else
			\caption{\label{#2}#3}
		\fi

		\begin{lrbox}{\@temptextboxa}
			\begin{minipage}{0.9\textwidth}
				\vspace*{1\myem}
				\begin{center}
					\begin{minipage}{0.9\textwidth}
					\txtboxfont\bgroup
}
{
					\egroup
					\end{minipage}\vspace*{1\myem}
					\txtfont
				\end{center}
			\end{minipage}
		\end{lrbox}
		\begin{center}
			\fcolorbox{textboxfgcolor}{textboxbgcolor}{\usebox{\@temptextboxa}}
		\end{center}
	\end{textboxb}
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%                        TABLES                        %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Table float structure
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\let\oldsubtable\subtable

\renewcommand{\subtable}[3]
{
	\ifx&#2& \oldsubtable[lof][]
	{
		\ifx&#1& \else \label{#1} \fi
		#3
	}
	\else \oldsubtable[lof][#2]
	{
		\ifx&#1& \else \label{#1} \fi
		#3
	}
	\fi
}

\renewenvironment{table}[3][]
{
	\belowcaptionskip=-0.8\myem
	\abovecaptionskip=0.5\myem

	\@float{table}[htbp]
		\ifx&#1& \def\my@auxcaptiontextshort{} \else \def\my@auxcaptiontextshort{#1} \fi
		\ifx&#2& \def\my@auxcaptionlabel{} \else \def\my@auxcaptionlabel{#2} \fi
		\def\my@auxcaptiontext{#3}
		\begin{center}
}
{
		\end{center}
		\ifx\my@auxcaptionlabel\empty
			\ifx\my@auxcaptiontextshort\empty
				\caption{\my@auxcaptiontext}
			\else
				\caption[\my@auxcaptiontextshort]{\my@auxcaptiontext}
			\fi
		\else
			\ifx\my@auxcaptiontextshort\empty
				\caption{\label{\my@auxcaptionlabel}\my@auxcaptiontext}
			\else
				\caption[\my@auxcaptiontextshort]{\label{\my@auxcaptionlabel}\my@auxcaptiontext}
			\fi
		\fi
	\end@float
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%                     EQUATIONS                        %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newif\if@mathcapbool \@mathcapboolfalse

\newlistof{equations}{loe}{\listequationname}
\newcommand{\eqncaption}[1]{\addcontentsline{loe}{table}{\numberline{\theequation} #1\string\relax}}

\renewcommand{\boxed}[1]{\fcolorbox{equationfgcolor}{equationbgcolor}{\m@th$\displaystyle#1$}}

\setlength{\belowdisplayskip}{1.5\myem}
\setlength{\belowdisplayshortskip}{1.5\myem}
\setlength{\abovedisplayskip}{-1.5\myem}
\setlength{\abovedisplayshortskip}{-1.5\myem}

\let\oldsubequations\subequations
\let\oldendsubequations\endsubequations

\renewenvironment{subequations}
{
	\setlength{\belowdisplayskip}{-1.5\myem}
	\setlength{\belowdisplayshortskip}{-1.5\myem}
	\setlength{\abovedisplayskip}{-1.5\myem}
	\setlength{\abovedisplayshortskip}{-1.5\myem}
	\oldsubequations
}
{
	\oldendsubequations
	\vspace*{1em}
}

\renewenvironment{equation}[2][]
{
	\incr@eqnum

	\ifx&#1& \else \label{#1} \fi
	\ifx&#2& \@mathcapboolfalse \else \@mathcapbooltrue \eqncaption{#2} \fi
	\mathdisplay@push
	\st@rredfalse \global\@eqnswtrue
	\mathdisplay{equation}
}{
	\endmathdisplay{equation}
	\mathdisplay@pop
	\ignorespacesafterend
}

\renewenvironment{equation*}
{
	\mathdisplay@push
	\st@rredtrue \global\@eqnswfalse
	\mathdisplay{equation*}
}{
	\endmathdisplay{equation*}
	\mathdisplay@pop
	\ignorespacesafterend
}

\newenvironment{multiequations}
{
	\setlength{\belowdisplayskip}{-2\myem}
	\setlength{\belowdisplayshortskip}{-2\myem}
	\refstepcounter{equation}
	\protected@edef\theparentequation{\theequation}
	\setcounter{parentequation}{\value{equation}}
	\setcounter{equation}{0}
	\def\theequation{\theparentequation\alph{equation}}
	\ignorespaces
	\noindent
}{
	\setcounter{equation}{\value{parentequation}}
	\ignorespacesafterend
}

\DeclareRobustCommand{\[}{\begin{equation*}}
\DeclareRobustCommand{\]}{\end{equation*}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%                       LISTS                          %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%




\newenvironment{functionality}
{
	\bgroup
	\renewcommand\baselinestretch{1.3}
  \typeout{Begining functionality}
  \par\relax
  \ifnum
    \@enumdepth >3 \@toodeep
  \else
    \advance\@enumdepth \@ne
    \def\@enumctr{enum\romannumeral\the\@enumdepth}
    \list{\csname label\@enumctr\endcsname}
    {
			\small
      \partopsep=0\myem \topsep=\@listinterlined \itemsep=\@listinterlined \parsep=\@listinterlined
      \advance\topsep by .3\myem
      \advance\itemsep by .15\myem
      \itemindent=0\myem
      \rightmargin=5\myex
      \leftmargin=8\myex
      \labelsep=1\myex \labelwidth=3\myex
      \usecounter{\@enumctr}
      \renewcommand*{\labelenumi}{\textbf{F-\theenumi.--}}
      \renewcommand*{\theenumii}{\arabic{enumii}}
      \renewcommand*{\labelenumii}{\textbf{F-\theenumi.\theenumii.--}}
      \renewcommand*{\theenumiii}{\arabic{enumiii}}
      \renewcommand*{\labelenumiii}{\textbf{F-\theenumi.\theenumii.\theenumiii.--}}
    }
  \fi
}
{
  \endlist
  \typeout{Ending functionality list}
  \egroup
}


\newenvironment{objetive}
{
	\bgroup
	\renewcommand\baselinestretch{1.3}
  \typeout{Begining objetive}
  \par\relax
  \ifnum
    \@enumdepth >3 \@toodeep
  \else
    \advance\@enumdepth \@ne
    \def\@enumctr{enum\romannumeral\the\@enumdepth}
    \list{\csname label\@enumctr\endcsname}
    {
			\small
      \partopsep=0\myem \topsep=\@listinterlined \itemsep=\@listinterlined \parsep=\@listinterlined
      \advance\topsep by .3\myem
      \advance\itemsep by .15\myem
      \itemindent=0\myem
      \rightmargin=5\myex
      \leftmargin=8\myex
      \labelsep=1\myex \labelwidth=3\myex
      \usecounter{\@enumctr}
      \renewcommand*{\labelenumi}{\textbf{O-\theenumi.--}}
      \renewcommand*{\theenumii}{\arabic{enumii}}
      \renewcommand*{\labelenumii}{\textbf{O-\theenumi.\theenumii.--}}
      \renewcommand*{\theenumiii}{\arabic{enumiii}}
      \renewcommand*{\labelenumiii}{\textbf{O-\theenumi.\theenumii.\theenumiii.--}}
    }
  \fi
}
{
  \endlist
  \typeout{Ending objetive list}
  \egroup
}

\newenvironment{functional}
{
	\bgroup
	\renewcommand\baselinestretch{1.3}
  \typeout{Begining enumeration}
  \ifnum
    \@enumdepth >3 \@toodeep
  \else
    \advance\@enumdepth \@ne
    \def\@enumctr{enum\romannumeral\the\@enumdepth}
    \list{\csname label\@enumctr\endcsname}
    {
			\small
      \partopsep=0\myem \topsep=\@listinterlined \itemsep=\@listinterlined \parsep=\@listinterlined
      \advance\topsep by .3\myem
      \advance\itemsep by .15\myem
      \itemindent=0\myem
      \rightmargin=5\myex
      \leftmargin=8\myex
      \labelsep=1\myex \labelwidth=3\myex
      \usecounter{\@enumctr}
      \renewcommand*{\labelenumi}{\textbf{RF-\theenumi.--}}
      \renewcommand*{\theenumii}{\arabic{enumii}}
      \renewcommand*{\labelenumii}{\textbf{RF-\theenumi.\theenumii.--}}
      \renewcommand*{\theenumiii}{\arabic{enumiii}}
      \renewcommand*{\labelenumiii}{\textbf{RF-\theenumi.\theenumii.\theenumiii.--}}
    }
  \fi
}
{
                \endlist
        \typeout{Ending enumeration}
        \egroup
}


\newenvironment{nonfunctional}
{
	\bgroup
	\renewcommand\baselinestretch{1.3}
  \typeout{Begining nonfunctional}
  \ifnum
    \@enumdepth >3 \@toodeep
  \else
    \advance\@enumdepth \@ne
    \def\@enumctr{enum\romannumeral\the\@enumdepth}
    \list{\csname label\@enumctr\endcsname}
    {
			\small
      \partopsep=0\myem \topsep=\@listinterlined \itemsep=\@listinterlined \parsep=\@listinterlined
      \advance\topsep by .3\myem
      \advance\itemsep by .15\myem
      \itemindent=0\myem
      \rightmargin=5\myex
      \leftmargin=8\myex
      \labelsep=1\myex \labelwidth=3\myex
      \usecounter{\@enumctr}
      \renewcommand*{\labelenumi}{\textbf{RNF-\theenumi.--}}
      \renewcommand*{\theenumii}{\arabic{enumii}}
      \renewcommand*{\labelenumii}{\textbf{RNF-\theenumi.\theenumii.--}}
      \renewcommand*{\theenumiii}{\arabic{enumiii}}
      \renewcommand*{\labelenumiii}{\textbf{RNF-\theenumi.\theenumii.\theenumiii.--}}
    }
  \fi
}
{
  \endlist
  \typeout{Ending nonfunctional}
  \egroup
}

\renewenvironment{enumerate}
{
	\bgroup
	\renewcommand\baselinestretch{1.3}
  \typeout{Begining enumeration}
  \ifnum
    \@enumdepth >3 \@toodeep
  \else
    \advance\@enumdepth \@ne
    \def\@enumctr{enum\romannumeral\the\@enumdepth}
    \list{\csname label\@enumctr\endcsname}
    {
			\small
      \partopsep=0\myem \topsep=\@listinterlined \itemsep=\@listinterlined \parsep=\@listinterlined
      \advance\topsep by .3\myem
      \advance\itemsep by .15\myem
      \itemindent=0\myem
      \rightmargin=5\myex
      \leftmargin=8\myex
      \labelsep=1\myex \labelwidth=0\myex
      \usecounter{\@enumctr}
      \renewcommand*{\labelenumi}{\theenumi.--}
      \renewcommand*{\theenumii}{\arabic{enumii}}
      \renewcommand*{\labelenumii}{\theenumi.\theenumii.--}
      \renewcommand*{\theenumiii}{\arabic{enumiii}}
      \renewcommand*{\labelenumiii}{\theenumi.\theenumii.\theenumiii.--}
    }
  \fi
}
{
  \endlist
  \typeout{Ending enumeration}
  \egroup
}

\renewenvironment{itemize}
{
	\bgroup
	\renewcommand\baselinestretch{1.3}
  \typeout{Begining itemize}
  \ifnum
    \@itemdepth >3 \@toodeep
  \else
	  \advance\@itemdepth \@ne
	  \def\@itemctr{item\romannumeral\the\@itemdepth}
	  \list{\csname label\@itemctr\endcsname}
	  {
			\small
      \partopsep=0\myem \topsep=\@listinterlined \itemsep=\@listinterlined \parsep=\@listinterlined
      \advance\topsep by .3\myem
      \advance\itemsep by .15\myem
      \itemindent=0\myem
      \rightmargin=5\myex
      \leftmargin=6\myex
      \labelsep=1\myex \labelwidth=0\myex
      \renewcommand*{\labelitemi}{$\bullet$}
      \renewcommand*{\labelitemii}{$\circ$}
      \renewcommand*{\labelitemiii}{$\diamond$}
	  }
  \fi
}
{
  \endlist
  \typeout{Ending itemize}
  \egroup
}


\newenvironment{simplelist}
{
	\bgroup
	\renewcommand\baselinestretch{1.3}
  \typeout{Begining thesislist}
  \ifnum
    \@itemdepth >3 \@toodeep
  \else
		\small
    \advance\@itemdepth \@ne
    \def\@itemctr{item\romannumeral\the\@itemdepth}
    \list{}
    {
			\small
      \partopsep=0\myem \topsep=\@listinterlined \itemsep=\@listinterlined \parsep=\@listinterlined
      \advance\topsep by .3\myem
      \advance\itemsep by .15\myem
      \itemindent=0\myem
      \rightmargin=5\myex
      \leftmargin=5\myex
    }
  \fi
}
{
  \endlist
  \typeout{Ending thesislist}
  \egroup
}


\renewenvironment{description}
{
	\bgroup
	\renewcommand\baselinestretch{1.3}
  \typeout{Begining description}
  \par\relax
  \list{}
  {
%		\small
    \partopsep=0\myem \topsep=\@listinterlined \itemsep=\@listinterlined \parsep=\@listinterlined
    \advance\topsep by .3\myem
    \advance\itemsep by .15\myem
    \itemindent=0\myex
    \leftmargin=8\myex
    \rightmargin=5\myex
    \labelsep=2\myex \labelwidth=2\myex
    \renewcommand*{\makelabel}[1]{\color{descriptioncolor} \textbf{##1}}
  }

}
{
        \endlist
        \typeout{Ending description list}
        \egroup
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%                       BUDGET                         %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\if@languagespa
	\def\unitarycost{Coste Unitario}
	\def\amount{Cantidad}
	\def\totalcost{Cantidad Total}
	\def\concepttitle{Concepto}
	\def\subtotaltext{Subtotal}
	\def\totaltext{Total}
\else
	\def\unitarycost{Unitary cost}
	\def\amount{Amount}
	\def\totalcost{Total cost}
	\def\concepttitle{Concept}
	\def\subtotaltext{Sub-Total}
	\def\totaltext{Total}
\fi

\def\separator{ & & & \\}

\def\budgettitle#1{\large{{\color{maincolor}\textbf{#1}}} & & & \\}

\def\cEUR#1{\if&#1& \empty \else \EUR{#1} \fi}

\def\concept#1#2#3#4{\phantom{ZZ}#1 & \cEUR{#2} & #3 & \cEUR{#4} \\ }
\def\subconcept#1#2#3#4{\phantom{ZZZZ}#1 & \cEUR{#2} & #3 & \cEUR{#4} \\ }
\def\subtotal#1{\phantom{ZZ}\textsc{\textbf{\subtotaltext}} & & & \textbf{\EUR{#1}} \\ \cline{4-4}}
\def\total#1{ \LARGE{\textsc{\textbf{\color{maincolor}\totaltext}}} & & \multicolumn{2}{r}{\LARGE{\textbf{\color{maincolor}\EUR{#1}}}} \\ \hline}

\newenvironment{budget}
{
	\begin{center}
		\begin{longtable}{p{.45\textwidth}rrr}
			\hline
			\textbf{\concepttitle} & \textbf{\unitarycost} & \textbf{\amount} & \textbf{\totalcost} \\
			\hline\hline
			\endhead
}
{
		\end{longtable}
	\end{center}
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%                        CODE                          %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Code listing macros
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\renewcommand{\lstlistlistingname}{\@auxvarcodeindex}
\renewcommand{\lstlistingname}{\@auxvarcode}

\lstdefinestyle{bashsty}{
	tabsize=4,commentstyle=\color{commentcolor}, columns=fullflexible, basicstyle=\codefont\footnotesize, breaklines=true,
	breakatwhitespace=true, numbersep=3\myex, stepnumber=1, numbers=none, frame=single, backgroundcolor=\color{codebgcolor},
	rulecolor=\color{codefgcolor},	xleftmargin=0.07\textwidth, xrightmargin=0.07\textwidth, numberstyle=\txtfont\footnotesize\bfseries,
	captionpos=b, abovecaptionskip=0.7\myem,texcl=false, aboveskip = 1\myem,belowskip=-1\myem,	framexleftmargin=0.02\textwidth,
	framexrightmargin=0.02\textwidth,mathescape=false, framextopmargin=1\myem,  framexbottommargin=1\myem, belowcaptionskip=1.2\myem, upquote=true,
	literate={*}{{\char42}}1 {-}{{\char45}}1
					 {á}{{\'a}}1 {Á}{{\'A}}1
					 {é}{{\'e}}1 {É}{{\'E}}1
					 {í}{{\'i}}1 {Í}{{\'I}}1
					 {ó}{{\'o}}1 {Ó}{{\'O}}1
					 {ú}{{\'u}}1 {Ú}{{\'U}}1
					 {ñ}{{\~n}}1 {Ñ}{{\~N}}1
					 {¡}{{!`}}1 {¿}{{?`}}1
}

\lstdefinestyle{numbered}{
	tabsize=4,commentstyle=\color{commentcolor}, columns=fullflexible, basicstyle=\codefont\footnotesize, breaklines=true,
	breakatwhitespace=true, numbersep=3\myex, stepnumber=1 ,numbers=left,	frame=single, backgroundcolor=\color{codebgcolor},
	rulecolor=\color{codefgcolor}, xleftmargin=0.07\textwidth,	xrightmargin=0.07\textwidth, numberstyle=\txtfont\footnotesize\bfseries,
	texcl=false, aboveskip=1\myem,	belowskip=-1\myem,	framexleftmargin=0.01\textwidth,  framexrightmargin=0.01\textwidth, mathescape=true,
	framextopmargin=1\myem, framexbottommargin=1\myem, belowcaptionskip=1.2\myem, upquote=true,
	literate={*}{{\char42}}1 {-}{{\char45}}1
					 {á}{{\'a}}1 {Á}{{\'A}}1
 					 {é}{{\'e}}1 {É}{{\'E}}1
 					 {í}{{\'i}}1 {Í}{{\'I}}1
 					 {ó}{{\'o}}1 {Ó}{{\'O}}1
 					 {ú}{{\'u}}1 {Ú}{{\'U}}1
					 {ñ}{{\~n}}1 {Ñ}{{\~N}}1
					 {¡}{{!`}}1 {¿}{{?`}}1
}

\lstdefinestyle{nonumbered}{
	tabsize=4,commentstyle=\color{commentcolor}, columns=fullflexible, basicstyle=\codefont\footnotesize, breaklines=true,
	breakatwhitespace=true, numbersep=3\myex, stepnumber=1, numbers=none, frame=single, backgroundcolor=\color{codebgcolor},
	rulecolor=\color{codefgcolor}, xleftmargin=0.07\textwidth, xrightmargin=0.07\textwidth, numberstyle=\txtfont\footnotesize\bfseries,
	texcl=false, aboveskip=1\myem, belowskip=-1\myem,	framexleftmargin=0.01\textwidth,  framexrightmargin=0.01\textwidth, mathescape=true,
	framextopmargin=1\myem, framexbottommargin=1\myem, belowcaptionskip=1.2\myem, upquote=true,
	literate={*}{{\char42}}1 {-}{{\char45}}1
					 {á}{{\'a}}1 {Á}{{\'A}}1
 					 {é}{{\'e}}1 {É}{{\'E}}1
 					 {í}{{\'i}}1 {Í}{{\'I}}1
 					 {ó}{{\'o}}1 {Ó}{{\'O}}1
 					 {ú}{{\'u}}1 {Ú}{{\'U}}1
					 {ñ}{{\~n}}1 {Ñ}{{\~N}}1
					 {¡}{{!`}}1 {¿}{{?`}}1
}

\lstdefinestyle{pseudonumbered}{
	tabsize=4,commentstyle=\color{commentcolor}, columns=fullflexible,
	basicstyle=\codefont\footnotesize, breaklines=true, breakatwhitespace=true,numbersep=3\myex, stepnumber=1,numbers=none,
	frame=single, backgroundcolor=\color{codebgcolor}, rulecolor=\color{codefgcolor},
	literate={:=}{{$\gets$}}1 {<=}{{$\leq$}}1 {>=}{{$\geq$}}1 {<>}{{$\neq$}}1, morekeywords=[2]{all,return},
	xleftmargin=0.07\textwidth, xrightmargin=0.07\textwidth, numberstyle=\txtfont\footnotesize\bfseries,
	captionpos=b, abovecaptionskip=0.7\myem,texcl=false, aboveskip = 1\myem,belowskip=-1\myem,
	framexleftmargin=0.02\textwidth,  framexrightmargin=0.02\textwidth,mathescape=true,
	framextopmargin=1\myem,  framexbottommargin=1\myem, belowcaptionskip=1.2\myem, upquote=true,
	literate={*}{{\char42}}1 {-}{{\char45}}1
					 {á}{{\'a}}1 {Á}{{\'A}}1
 					 {é}{{\'e}}1 {É}{{\'E}}1
 					 {í}{{\'i}}1 {Í}{{\'I}}1
 					 {ó}{{\'o}}1 {Ó}{{\'O}}1
 					 {ú}{{\'u}}1 {Ú}{{\'U}}1
					 {ñ}{{\~n}}1 {Ñ}{{\~N}}1
					 {¡}{{!`}}1 {¿}{{?`}}1
}

\lstdefinestyle{pseudononumbered}{
	tabsize=4,commentstyle=\color{commentcolor}, columns=fullflexible,
	basicstyle=\codefont\footnotesize, breaklines=true, breakatwhitespace=true,numbersep=3\myex, stepnumber=1,numbers=none,
	frame=single, backgroundcolor=\color{codebgcolor}, rulecolor=\color{codefgcolor},
	literate={:=}{{$\gets$}}1 {<=}{{$\leq$}}1 {>=}{{$\geq$}}1 {<>}{{$\neq$}}1, morekeywords=[2]{all,return},
	xleftmargin=0.07\textwidth, xrightmargin=0.07\textwidth, numberstyle=\txtfont\footnotesize\bfseries,
	captionpos=b, abovecaptionskip=0.7\myem,texcl=false, aboveskip = 1\myem,belowskip=-1\myem,
	framexleftmargin=0.02\textwidth,  framexrightmargin=0.02\textwidth,mathescape=true,
	framextopmargin=1\myem,  framexbottommargin=1\myem, belowcaptionskip=1.2\myem, upquote=true,
	literate={*}{{\char42}}1 {-}{{\char45}}1
					 {á}{{\'a}}1 {Á}{{\'A}}1
 					 {é}{{\'e}}1 {É}{{\'E}}1
 					 {í}{{\'i}}1 {Í}{{\'I}}1
 					 {ó}{{\'o}}1 {Ó}{{\'O}}1
 					 {ú}{{\'u}}1 {Ú}{{\'U}}1
					 {ñ}{{\~n}}1 {Ñ}{{\~N}}1
					 {¡}{{!`}}1 {¿}{{?`}}1
}

\floatstyle{plain}
\newfloat{codefloat}{hptb}{ltb}[subsubsection]

\newcommand{\@allcodes}[8][]{
	\begin{codefloat}
		\ifx&#1& \else \lstset{label=#1} \fi
		\ifx&#7& \else \lstset{firstnumber=#7} \fi
		\ifx&#8& \lstset{language=Pascal} \else \lstset{language=#8} \fi
		\ifx&#2& \lstset{caption={#3}} \else \lstset{caption=[#2]{#3}} \fi
		\ifx&#7& \lstset{style=nonumbered} \else \lstset{style=numbered} \fi

		\ifx&#5&
			\ifx&#6& \vbox{\lstinputlisting{\@auxcodesdir/#4}}
			\else \vbox{\lstinputlisting[lastline=#6]{\@auxcodesdir/#4}}
			\fi
		\else
			\ifx&#6& \vbox{\lstinputlisting[firstline=#5]{#4}}
			\else \vbox{\lstinputlisting[firstline=#5,lastline=#6]{\@auxcodesdir/#4}}
			\fi
		\fi
	\end{codefloat}
}



\newcommand{\Code}[8][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{#8}}
\newcommand{\AdaCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{Ada}}
\newcommand{\ASMCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{[x86asm]Assembler}}
\newcommand{\ASMMotorolaCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{[Motorola68k]Assembler}}
\newcommand{\CCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{C}}
\newcommand{\CPPCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{C++}}
\newcommand{\CSharpCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{[Sharp]C}}
\newcommand{\GnuplotCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{Gnuplot}}
\newcommand{\HaskellCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{Haskell}}
\newcommand{\HTMLCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{HTML}}
\newcommand{\JavaCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{Java}}
\newcommand{\LaTeXCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{[AlLaTeX]TeX}}
\newcommand{\LispCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{Lisp}}
\newcommand{\MakeCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{make}}
\newcommand{\MathematicaCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{Mathematica}}
\newcommand{\MatlabCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{Matlab}}
\newcommand{\OctaveCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{Octave}}
\newcommand{\PascalCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{Pascal}}
\newcommand{\PerlCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{Perl}}
\newcommand{\PHPCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{PHP}}
\newcommand{\PythonCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{Python}}
\newcommand{\RCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{R}}
\newcommand{\RubyCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{Ruby}}
\newcommand{\ScilabCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{Scilab}}
\newcommand{\SQLCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{SQL}}
\newcommand{\VHDLCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{VHDL}}
\newcommand{\XMLCode}[7][]{\@allcodes[#1]{#2}{#3}{#4}{#5}{#6}{#7}{XML}}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%                     ALGORITHM                        %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\floatname{algorithmb}{\@auxvaralgorithm}
\floatstyle{plain}
\newfloat{algorithmb}{htbp}{loa}[chapter]

\newsavebox{\@tempalgorithma}

\newenvironment{algorithm}[3][]
{
	\renewcommand{\abovecaptionskip}{0\myem}
	\begin{algorithmb}
			\ifx&#1&
			\ifx&#2&
				\caption{#3}
			\else
				\caption[#2]{#3}
			\fi
		\else
			\ifx&#2&
				\caption{\label{#1}#3}
			\else
				\caption[#2]{\label{#1}#3}
			\fi
		\fi
		\begin{lrbox}{\@tempalgorithma}
			\begin{minipage}{0.9\textwidth}
				\vspace*{0.5\myem}
				\@algocf@start
					\SetVline
					\@ResetCounterIfNeeded
					\algocf@linesnumbered
					\txtfont
					\begin{footnotesize}
}
{
					\end{footnotesize}
				\@algocf@finish
				\vspace*{0.5\myem}
			\end{minipage}
		\end{lrbox}
		\begin{footnotesize}
			\begin{center}
				\fcolorbox{codefgcolor}{codebgcolor}{\usebox{\@tempalgorithma}}
			\end{center}
		\end{footnotesize}
	\end{algorithmb}
}

\newenvironment{algorithmN}[3][]
{
	\renewcommand{\abovecaptionskip}{0\myem}
	\LinesNumbered
	\setlength{\algomargin}{0.8\myem}
	\SetNlSkip{0.033\textwidth}
	\SetNlSty{algonumfont}{}{}
	\begin{algorithmb}
		\ifx&#1&
			\ifx&#2&
				\caption{#3}
			\else
				\caption[#2]{#3}
			\fi
		\else
			\ifx&#2&
				\caption{\label{#1}#3}
			\else
				\caption[#2]{\label{#1}#3}
			\fi
		\fi
		\hspace*{0.3\textwidth}
		\begin{lrbox}{\@tempalgorithma}
			\begin{minipage}{0.9\textwidth}
				\vspace*{0.5\myem}
				\@algocf@start
					\@ResetCounterIfNeeded
					\algocf@linesnumbered
					\begin{footnotesize}
}
{
					\end{footnotesize}
				\@algocf@finish
				\vspace*{0.5\myem}
			\end{minipage}
		\end{lrbox}
		\begin{footnotesize}
			\begin{center}
				\fcolorbox{codefgcolor}{codebgcolor}{\usebox{\@tempalgorithma}}
			\end{center}
		\end{footnotesize}
	\end{algorithmb}
	\LinesNotNumbered
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%                     CITATIONS                        %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Large citations and citations on line
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newenvironment{largecitation}[1][]
{
  \par
  \ifx&#1&
    \def\@auxcitevar{\empty}%
  \else
    \def\@auxcitevar{#1}%
  \fi
  \begin{center}
    \begin{minipage}{0.8\textwidth}
    	`` \textit\bgroup
}
{
      \egroup ''
    	\ifx\@auxcitevar\empty\mbox{}\par\else\\[1\myem]\mbox{}\hfill\@auxcitevar\fi
    \end{minipage}\vspace*{1\myem}
  \end{center}
}

\newcommand{\onlinecitation}[2][]
{
  \textit{``#2''}\ifx&#1&\empty\else \mbox{} (#1)\fi
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%                       TEXTS                          %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\def\@auxuniversityfaculty
{
	\begin{center}
			\begin{Large}\textbf{UNIVERSIDAD AUTÓNOMA DE MADRID}\end{Large} \\
			\begin{large}\textbf{\MakeUppercase{\@faculty}}\end{large}\vspace*{1\myem}
	\end{center}

	\if@languagespa
		\if@tfgwork
			\pdfmetavalues{\@author}{\@titleaux}{Trabajo fin de Grado}{\@auxkeywords,\@auxpalabrasclave}
		\else
			\if@tfmwork
				\pdfmetavalues{\@author}{\@titleaux}{Trabajo fin de Máster}{\@auxkeywords,\@auxpalabrasclave}
			\else
				\pdfmetavalues{\@author}{\@titleaux}{Tesis}{\@auxkeywords,\@auxpalabrasclave}
			\fi 
		\fi 
	\else
		\if@tfgwork
			\pdfmetavalues{\@author}{\@titleaux}{Bachelor thesis}{\@auxkeywords,\@auxpalabrasclave}
		\else
			\if@tfmwork
				\pdfmetavalues{\@author}{\@titleaux}{Master thesis}{\@auxkeywords,\@auxpalabrasclave}
			\else
				\pdfmetavalues{\@author}{\@titleaux}{Thesis}{\@auxkeywords,\@auxpalabrasclave}
			\fi 
		\fi 
	\fi
}

\if@languagespa
	\def\@auxvarheadtitle
	{
		\if@tfgwork
			\begin{center}
				\begin{small}
					Proyecto para la obtención del título de \\
					Grado en \@levelin \\
					por la Universidad Autónoma de Madrid \\[1\myem]
					\ifx\@speaker\empty\else
						Ponente del trabajo fin de grado: \\ \@speaker \\[1\myem]
					\fi
					Tutor del trabajo fin de grado: \\ \@advisor \\ \mbox{}
					\if@coadvisorbool Cotutor del trabajo fin de grado: \\ \@coadvisor \\ \mbox{}\fi
				\end{small}
			\end{center}
		\else	
			\if@tfmwork
				\pdfmetavalues{\@author}{\@titleaux}{Trabajo fin de Máster}{\@auxkeywords,\@auxpalabrasclave}
				\begin{center}
					\begin{small}
						Proyecto para la obtención del título de \\
						Máster en \@levelin \\
						por la Universidad Autónoma de Madrid \\[1\myem]
						\ifx\@speaker\empty\else
							Ponente del trabajo fin de máster: \\ \@speaker \\[1\myem]
						\fi
						Tutor del trabajo fin de máster: \\ \@advisor \\ \mbox{}
						\if@coadvisorbool Cotutor del trabajo fin de máster: \\ \@coadvisor \\ \mbox{}\fi
					\end{small}
				\end{center}
			\else
				\pdfmetavalues{\@author}{\@titleaux}{Tesis}{\@auxkeywords,\@auxpalabrasclave}
				\begin{center}
					\begin{small}
						Proyecto para la obtención del título de \\
						Doctor en \@levelin \\
						por la Universidad Autónoma de Madrid \\[1\myem]
						Director de tesis: \\ \@advisor \\ \mbox{}
						\if@coadvisorbool Cotutor de tesis: \\ \@coadvisor \\ \mbox{}\fi
					\end{small}
				\end{center}
			\fi
		\fi
	}

\else

	\def\@auxvarheadtitle
	{
		\if@tfgwork
			\begin{center}
				\begin{small}
					Project to obtain bachelor degree in \\
					\@levelin \\
					by Universidad Autónoma de Madrid \\[1\myem]
					\ifx\@speaker\empty\else
						Speaker: \\ \@speaker \\[1\myem]
					\fi
					Advisor: \\ \@advisor \\ \mbox{}
					\if@coadvisorbool Coadvisor: \\ \@coadvisor \\ \mbox{}\fi
				\end{small}
			\end{center}
		\else \if@tfmwork
			\begin{center}
				\begin{small}
					Work to obtain master degree in \\
					\@levelin \\
					by Universidad Autónoma de Madrid \\[1\myem]
					\ifx\@speaker\empty\else
						Speaker: \\ \@speaker \\[1\myem]
					\fi
						Advisor: \\ \@advisor \\ \mbox{}
					\if@coadvisorbool Master thesis coadvisor: \\ \@coadvisor \\ \mbox{}\fi
				\end{small}
			\end{center}
		\else
			\begin{center}
				\begin{small}
					Thesis to obtain PhD. degree in \\
					\@levelin \\
					by Universidad Autónoma de Madrid \\[1\myem]
					Advisor: \\ \@advisor \\ \mbox{}
					\if@coadvisorbool Coadvisor: \\ \@coadvisor \\ \mbox{}\fi
				\end{small}
			\end{center}
		\fi \fi
	}
\fi

\def\allrightsreserved{\cleardoublepage}
\if@languagespa
	\if@copyrightbool
		\def\allrightsreserved
		{
			\mbox{} \\
			\textbf{Todos los derechos reservados.} \\[0.2\myex]
			Queda prohibida, salvo excepción prevista en la Ley, cualquier \\
			forma de reproducción, distribución comunicación pública \\
			y transformación de esta obra sin contar con la autorización \\
			de los titulares de la propiedad intelectual. \\
			La infracción de los derechos mencionados puede ser constitutiva de\\
			delito contra la propiedad intelectual \textit{(arts. 270 y sgts. del Código Penal)}. \\[4\myex]
			DERECHOS RESERVADOS \\
			{\copyright} {\@copyrightdate} por UNIVERSIDAD AUTÓNOMA DE MADRID \\
			Francisco Tomás y Valiente, n$^o$ 1 \\
			Madrid, 28049 \\
			Spain
		}
	\fi
	\if@copyleftbool
		\def\allrightsreserved
		{
			\begin{minipage}{0.7\textwidth}
			\mbox{} \\
			\textbf{Algunos derechos reservados.} \\[0.2\myex]
			Este trabajo está bajo licencia Creative Commons\\
			\href{http://creativecommons.org/licenses/by-nc-sa/3.0/}{http://creativecommons.org/licenses/by-nc-sa/3.0/} \\[0.2\myex]
			Esta obra se puede copiar, distribuir y comunicar públicamente la obra así como crear obras derivadas bajo las siguientes condiciones:
			\begin{scriptsize}
			\begin{itemize}
			\begin{scriptsize}
				\item Debe reconocer los créditos manteniendo la autoría original y añadiendo la autoría de las modificaciones indicando de forma expresa y bien visible que el autor original no manifiesta ningún tipo de apoyo a as modificaciones realizadas así como al uso que se da de esta obra.
				\item No se puede utilizar esta obra con fines comerciales.
				\item Las modificaciones o ediciones de esta obra deben compartirse bajo una licencia idéntica a esta.
			\end{scriptsize}
			\end{itemize}
			\end{scriptsize}
			La infracción de los derechos mencionados puede ser constitutiva de\\
			delito contra la propiedad intelectual \textit{(arts. 270 y sgts. del Código Penal)}. \\[4\myex]
			DERECHOS RESERVADOS \\
			{\copyright} {\@copyrightdate} por UNIVERSIDAD AUTÓNOMA DE MADRID \\
			Francisco Tomás y Valiente, nº 1 \\
			Madrid, 28049 \\
			Spain
			\end{minipage}
		}
	\fi
\else
	\if@copyrightbool
		\def\allrightsreserved
		{
			\mbox{} \\
			\textbf{All rights reserved.} \\[0.2\myex]
			No reproduction in any form of this book, in whole or in part \\
			(except for brief quotation in critical articles or reviews), \\
			may be made without written authorization from the publisher. \\[4\myex]
			{\copyright} {\@copyrightdate} by UNIVERSIDAD AUTÓNOMA DE MADRID \\
			Francisco Tom\'as y Valiente, n$^o$ 1 \\
			Madrid, 28049 \\
			Spain
		}
	\fi
	\if@copyleftbool
		\def\allrightsreserved
		{
			\begin{minipage}{0.7\textwidth}
			\mbox{} \\
			\textbf{Some rights reserved} \\[0.2\myex]
			This work is licensed under a Creative Commons\\
			Attribution-NonCommercial-ShareAlike 3.0 License.\\
			\href{http://creativecommons.org/licenses/by-nc-sa/3.0/}{http://creativecommons.org/licenses/by-nc-sa/3.0/} \\[0.2\myex]
			You are free to share (copy, distribute and transmit) and to modify the work\\ under the following conditions:
			\begin{itemize}
				\item You must attribute the work in the manner specified by the author\\ or licensor (but not in any way that suggests that they endorse you or\\ your use of the work).
				\item You may not use this work for commercial purposes.
				\item If you alter, transform, or build upon this work, you may distribute\\ the resulting work only under the same or similar license to this one.
			\end{itemize}
			RIGHTS RESERVED \\
			{\copyright} {\@copyrightdate} por UNIVERSIDAD AUTÓNOMA DE MADRID \\
			Francisco Tomás y Valiente, nº 1 \\
			Madrid, 28049 \\
			Spain
			\end{minipage}
		}
	\fi
\fi


	\def\printedon
	{
		\if@languagespa
			\mbox{} \\[4\myex]
			{\bfseries \@author} \\
			{\bfseries \textit{\@titleaux}} \\[4\myex]
			{\bfseries \@author} \\
			\@privateaddress \\[4\myex]
			IMPRESO EN ESPAÑA -- PRINTED IN SPAIN
		\else
			\mbox{} \\[4\myex]
			{\bfseries \@author} \\
			{\bfseries \textit{\@titleaux}} \\[4\myex]
			{\bfseries \@author} \\
			\@privateaddress \\[4\myex]
			PRINTED IN SPAIN
		\fi
	}

\def\mypalabrasclave
{
	\begin{flushleft}
		\color{maincolor}
		\txtchapfont
		Palabras clave
		\vspace{-.58\myem}
	\end{flushleft}
	\thickhrulefill
	\color{black}

	\@auxpalabrasclave
}

\def\mykeywords
{
	\begin{flushleft}
		\color{maincolor}
		\txtchapfont
		Keywords
		\vspace{-.58\myem}
	\end{flushleft}
	\thickhrulefill
	\color{black}

	\@auxkeywords
}

\if@languagespa
	\def\pretexts
	{
		\ifx\@prefacefile\empty\else\chapter*{Prefacio}{\@prefacefile}\fi
		\ifx\@ackfile\empty\else\chapter*{Agradecimientos}{\@ackfile}\fi
		\ifx\@resumenfile\empty\else\chapter*{Resumen}{\@resumenfile}\vfill\mypalabrasclave\fi
		\ifx\@abstractfile\empty\else\chapter*{Abstract}{\@abstractfile}\vfill\mykeywords\fi
	}
\else
	\def\pretexts
	{
		\ifx\@prefacefile\empty\else\chapter*{Prefacio}{\@prefacefile}\fi
		\ifx\@ackfile\empty\else\chapter*{Agradecimientos}{\@ackfile}\fi
		\ifx\@resumenfile\empty\else\chapter*{Resumen}{\@resumenfile}\vfill\mypalabrasclave\fi
		\ifx\@abstractfile\empty\else\chapter*{Abstract}{\@abstractfile}\vfill\mykeywords\fi
	}
\fi



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%                       GANTT                          %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newcommandtwoopt\taskbar[5][][]
{
	\ifx&#1&
		\ifx&#2&
			\ganttbar[bar height=.45, bar label font=\mdseries\footnotesize\color{complementarydarkone}, bar/.append style={draw=none, fill=complementaryone}, bar incomplete/.append style={fill=complementarylightone}, bar progress label font=\mdseries\scriptsize\color{complementaryone}]{#3}{#4}{#5}
		\else
			\ganttbar[progress=#2, bar height=.45, bar label font=\mdseries\footnotesize\color{complementarydarkone}, bar/.append style={draw=none, fill=complementaryone},	bar incomplete/.append style={fill=complementarylightone}, bar progress label font=\mdseries\scriptsize\color{complementaryone}]{#3}{#4}{#5}
		\fi
	\else
		\ifx&#2&
			\ganttbar[name=#1, bar height=.45, bar label font=\mdseries\footnotesize\color{complementarydarkone}, bar/.append style={draw=none, fill=complementaryone}, bar incomplete/.append style={fill=complementarylightone}, bar progress label font=\mdseries\scriptsize\color{complementaryone}]{#3}{#4}{#5}
		\else
			\ganttbar[progress=#2, name=#1, bar height=.45, bar label font=\mdseries\footnotesize\color{complementarydarkone}, bar/.append style={draw=none, fill=complementaryone}, bar incomplete/.append style={fill=complementarylightone}, bar progress label font=\mdseries\scriptsize\color{complementaryone}]{#3}{#4}{#5}
		\fi
	\fi
}

\newcommand\milestone[3][]
{
	\ifx&#1&
		\ganttmilestone[milestone/.append style={shape=ganttmilestone, fill=complementaryfour},	milestone label font=\bfseries\scriptsize\color{complementarydarkfour}]{#2}{#3}{#3}
	\else
		\ganttmilestone[milestone/.append style={shape=ganttmilestone, fill=complementaryfour}, milestone label font=\bfseries\scriptsize\color{complementarydarkfour},name=#1]{#2}{#3}{#3}
	\fi
}

\newcommand\FtoSlink[2]
{
	\ganttlink[
	link/.style={[-latex, thick, complementarysix, rounded corners=0.6\myex},
	link label font=\tiny\bfseries,
	link mid=.5, link bulge=0.6,
	link label node/.append style={below left=-2\mypt and 0\mypt}]{#1}{#2}
}

\setganttlinklabel{s-s}{}
\newcommand\StoSlink[2]
{
	\ganttlink[link type=s-s,
	link/.style={-latex, thick, complementarysix, rounded corners=0.6\myex},
	link label font=\tiny\bfseries,
	link mid=.5, link bulge=0.6,
	link label node/.append style={below left=-2\mypt and 0\mypt}]{#1}{#2}
}

\setganttlinklabel{f-f}{}
\newcommand\FtoFlink[2]
{
	\ganttlink[link type=f-f,
	link/.style={-latex, thick, complementarysix, rounded corners=0.6\myex},
	link label font=\tiny\bfseries,
	link mid=.5, link bulge=0.6,
	link label node/.append style={below left=-2\mypt and 0\mypt}]{#1}{#2}
}

\newcommandtwoopt\taskgroup[5][][]
{

	\ifx&#1&
		\ifx&#2&
			\ganttgroup[group height=.35, group label font=\bfseries\small\color{complementarydarktwo}, group/.append style={draw=none, fill=complementarytwo},
			group incomplete/.append style={fill=complementarylighttwo}, group progress label font=\bfseries\scriptsize\color{complementarytwo},
			group left shift=0, group right shift=0, group peaks tip position=0, group left shift=0, group right shift=0, group peaks tip position=0]{#3}{#4}{#5}
		\else
			\ganttgroup[progress=#2, group height=.35, group label font=\bfseries\small\color{complementarydarktwo}, group/.append style={draw=none, fill=complementarytwo},
			group incomplete/.append style={fill=complementarylighttwo}, group progress label font=\bfseries\scriptsize\color{complementarytwo},
			group left shift=0, group right shift=0, group peaks tip position=0]{#3}{#4}{#5}
		\fi
	\else
		\ifx&#2&
			\ganttgroup[name=#1, group height=.35, group label font=\bfseries\small\color{complementarydarktwo}, group/.append style={draw=none, fill=complementarytwo},
			group incomplete/.append style={fill=complementarylighttwo}, group progress label font=\bfseries\scriptsize\color{complementarytwo},
			group left shift=0, group right shift=0, group peaks tip position=0]{#3}{#4}{#5}
		\else
			\ganttgroup[progress=#2, name=#1, group height=.35, group label font=\bfseries\small\color{complementarydarktwo}, group/.append style={draw=none, fill=complementarytwo},
			group incomplete/.append style={fill=complementarylighttwo}, group progress label font=\bfseries\scriptsize\color{complementarytwo},
			group left shift=0, group right shift=0, group peaks tip position=0]{#3}{#4}{#5}
		\fi
	\fi
}


\newenvironment{gantt}[2]
{
\vspace*{-2\myem}\noindent\begin{ganttchart}[
	canvas/.append style={fill=none, draw=complementarylightone!50, line width=.75\mypt},y unit chart=1.3\myem,
	vgrid={*1{draw=complementarylightone!50, line width=.75\mypt, dotted, dash pattern=on 3.5\mypt off 4.5\mypt}},
	title/.style={draw=none, fill=none},
	title label font=\bfseries\scriptsize,
	title label node/.append style={below=7\mypt},
	include title in canvas=false,
	]{#1}{#2}

	\gantttitle[
	title label node/.append style={below left=3.38\myem and 1.5\myex}
	]{Semana:}{1} \\
	\gantttitlelist{#1,...,#2}{1} \\
}
{
	\end{ganttchart}
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%                      PLOTING                         %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


\if@gnuplotbool
\else
  \newenvironment{gnuplot}[1][]
	{
		\begin{Large}
			\textbf{\color{red}Undefined gnuplot option}
		\end{Large}\par
		\hbox to 0pt \bgroup \vbox to 0pt \bgroup \color{white}
		}
		{\egroup\egroup}
\fi


\pgfplotsset{
	legend style= {font=\footnotesize},
	x tick label style={font=\footnotesize},
	y tick label style={font=\footnotesize},
}

\newenvironment{xyplot}[6][north east]
{
	\setcounter{@ploti}{0}
	\begin{tikzpicture}
		\begin{axis}[
			title={#2},
			xlabel={#3},
			ylabel={#4},
			width=#5,
			height=#6,
			legend style={draw=none},
			legend pos=#1
			]
}
{
		\end{axis}
	\end{tikzpicture}
}

\newenvironment{loglogplot}[6][north east]
{
	\setcounter{@ploti}{0}
	\begin{tikzpicture}
		\begin{loglogaxis}[
			title={#2},
			xlabel={#3},
			ylabel={#4},
			width=#5,
			height=#6,
			legend style={draw=none},
			legend pos=#1
			]
}
{
		\end{loglogaxis}
	\end{tikzpicture}
}

\newenvironment{semilogxplot}[6][north east]
{
	\setcounter{@ploti}{0}
	\begin{tikzpicture}
		\begin{semilogxaxis}[
			title={#2},
			xlabel={#3},
			ylabel={#4},
			width=#5,
			height=#6,
			legend style={draw=none},
			legend pos=#1
			]
}
{
		\end{semilogxaxis}
	\end{tikzpicture}
}

\newenvironment{semilogyplot}[6][north east]
{
	\setcounter{@ploti}{0}
	\begin{tikzpicture}
		\begin{semilogyaxis}[
			title={#2},
			xlabel={#3},
			ylabel={#4},
			width=#5,
			height=#6,
			legend style={draw=none},
			legend pos=#1
				]
}
{
		\end{semilogyaxis}
	\end{tikzpicture}
}

\newcommand{\plotlined}[2]
{
	\stepcounter{@ploti}

	\addlegendentry{#2}
	\ifnum \value{@ploti}=1 \addplot[complementarytwo,line width=1pt] table {#1}; \fi
	\ifnum \value{@ploti}=2 \addplot[complementarythree,line width=1pt] table {#1}; \fi
	\ifnum \value{@ploti}=3 \addplot[complementaryfour,line width=1pt] table {#1}; \fi
	\ifnum \value{@ploti}=4 \addplot[complementaryone,line width=1pt] table {#1}; \fi
	\ifnum \value{@ploti}=5 \addplot[complementarysix,line width=1pt] table {#1}; \fi
	\ifnum \value{@ploti}=6 \addplot[complementaryseven,line width=1pt] table {#1}; \fi
	\ifnum \value{@ploti}=7 \addplot[complementaryeight,line width=1pt] table {#1}; \fi
	\ifnum \value{@ploti}=8 \addplot[complementaryfive,line width=1pt] table {#1}; \fi
}

\newcommand{\plotbaseline}[2]
{
\addplot[black,dashed,update limits=false]
coordinates {(#1,0) (#2,0)};
}

\newcommand{\plotdatalined}[2]
{
	\stepcounter{@ploti}

	\addlegendentry{#2}
	\ifnum \value{@ploti}=1 \addplot[mark=*,complementarytwo,line width=1pt] table {#1}; \fi
	\ifnum \value{@ploti}=2 \addplot[mark=square*,complementarythree,line width=1pt] table {#1}; \fi
	\ifnum \value{@ploti}=3 \addplot[mark=triangle*,complementaryfour,line width=1pt] table {#1}; \fi
	\ifnum \value{@ploti}=4 \addplot[mark=diamond*,complementarydarkone,line width=1pt] table {#1}; \fi
	\ifnum \value{@ploti}=5 \addplot[mark=pentagon*,complementarysix,line width=1pt] table {#1}; \fi
	\ifnum \value{@ploti}=6 \addplot[mark=ball*,complementaryseven,line width=1pt] table {#1}; \fi
	\ifnum \value{@ploti}=7 \addplot[mark=cube*,complementaryeight,line width=1pt] table {#1}; \fi
	\ifnum \value{@ploti}=8 \addplot[mark=x,complementarydarkfive,line width=1pt] table {#1}; \fi
}

\newcommand{\plotdata}[2]
{
	\stepcounter{@ploti}

	\addlegendentry{#2}
	\ifnum \value{@ploti}=1 \addplot[only marks,mark=*,complementarytwo] table {#1}; \fi
	\ifnum \value{@ploti}=2 \addplot[only marks,mark=square*,complementarythree] table {#1}; \fi
	\ifnum \value{@ploti}=3 \addplot[only marks,mark=triangle*,complementaryfour] table {#1}; \fi
	\ifnum \value{@ploti}=4 \addplot[only marks,mark=diamond*,complementaryone] table {#1}; \fi
	\ifnum \value{@ploti}=5 \addplot[only marks,mark=pentagon*,complementarysix] table {#1}; \fi
	\ifnum \value{@ploti}=6 \addplot[only marks,mark=ball*,complementaryseven] table {#1}; \fi
	\ifnum \value{@ploti}=7 \addplot[only marks,mark=cube*,complementaryeight] table {#1}; \fi
	\ifnum \value{@ploti}=8 \addplot[only marks,mark=x,complementaryfive] table {#1}; \fi
}

\newcommand{\plotfunction}[5][]
{
	\stepcounter{@ploti}
	\pgfplotsset{legend style={font=\normalsize}}

	\addlegendentry{#3}
	\if&#1&
		\ifnum \value{@ploti}=1 \addplot[complementarytwo,domain=#4:#5,samples=400,line width=1pt] {#2}; \fi
		\ifnum \value{@ploti}=2 \addplot[complementarythree,domain=#4:#5,samples=400,line width=1pt] {#2}; \fi
		\ifnum \value{@ploti}=3 \addplot[complementaryfour,domain=#4:#5,samples=400,line width=1pt] {#2}; \fi
		\ifnum \value{@ploti}=4 \addplot[complementaryone,domain=#4:#5,samples=400,line width=1pt] {#2}; \fi
		\ifnum \value{@ploti}=5 \addplot[complementarysix,domain=#4:#5,samples=400,line width=1pt] {#2}; \fi
		\ifnum \value{@ploti}=6 \addplot[complementaryseven,domain=#4:#5,samples=400,line width=1pt] {#2}; \fi
		\ifnum \value{@ploti}=7 \addplot[complementaryeight,domain=#4:#5,samples=400,line width=1pt] {#2}; \fi
		\ifnum \value{@ploti}=8 \addplot[complementaryfive,domain=#4:#5,samples=400,line width=1pt] {#2}; \fi
	\else
		\ifnum \value{@ploti}=1 \addplot[complementarytwo,domain=#4:#5,samples=#1,line width=1pt] {#2}; \fi
		\ifnum \value{@ploti}=2 \addplot[complementarythree,domain=#4:#5,samples=#1,line width=1pt] {#2}; \fi
		\ifnum \value{@ploti}=3 \addplot[complementaryfour,domain=#4:#5,samples=#1,line width=1pt] {#2}; \fi
		\ifnum \value{@ploti}=4 \addplot[complementaryone,domain=#4:#5,samples=#1,line width=1pt] {#2}; \fi
		\ifnum \value{@ploti}=5 \addplot[complementarysix,domain=#4:#5,samples=#1,line width=1pt] {#2}; \fi
		\ifnum \value{@ploti}=6 \addplot[complementaryseven,domain=#4:#5,samples=#1,line width=1pt] {#2}; \fi
		\ifnum \value{@ploti}=7 \addplot[complementaryeight,domain=#4:#5,samples=#1,line width=1pt] {#2}; \fi
		\ifnum \value{@ploti}=8 \addplot[complementaryfive,domain=#4:#5,samples=#1,line width=1pt] {#2}; \fi
	\fi
}



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%            BIBLIOGRAPHY AND REFERENCES               %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


\newcommand{\bibliographyconfig}[2][ieeetr]
{
	\@bibliographymodebooltrue
	\providecommand*\@bibstyleaux{#1}
	\providecommand*\@bibfileaux{#2}
}

\newdimen\bibspace
\setlength\bibspace\z@
\def\bibinterlined#1{\setlength\bibspace{#1}}

\renewenvironment{thebibliography}[1]
{
	\chapter*{\bibname}\thispagestyle{empty}
	\@mkboth{\MakeUppercase\bibname}{\MakeUppercase\bibname}
	\list{\@biblabel{\@arabic\c@enumiv}}
		{\settowidth\labelwidth{\@biblabel{#1}}
		\leftmargin\labelwidth
		\advance\leftmargin\labelsep
		\itemsep\bibspace
		\parsep\bibspace
		\@openbib@code
		\usecounter{enumiv}
		\let\p@enumiv\@empty
		\renewcommand\theenumiv{\@arabic\c@enumiv}}
	\sloppy
	\clubpenalty4000
	\@clubpenalty \clubpenalty
	\widowpenalty4000
	\sfcode`\.\@m
}
{
	\def\@noitemerr
	{\@latex@warning{Empty `thebibliography' environment}}
	\endlist
}


\newcommand{\thesisbibliography}
{
	\if@bibliographymodebool
		\bibliographystyle{\@bibstyleaux}
		\bibliography{\@bibfileaux}
		\addcontentsline{toc}{chapter}{\bibname}
	\fi
}

\crefname{algorithmb}{algoritmo}{algoritmos}
\Crefname{algorithmb}{Algoritmo}{Algoritmos}

\crefname{textboxb}{cuadro\ de\ texto}{cuadros\ de\ texto}
\Crefname{textboxb}{Cuadro\ de\ texto}{Cuadros\ de\ texto}

\crefname{subequation}{subecuación}{subecuaciones}
\Crefname{subequation}{Subecuación}{Subecuaciones}

\crefname{subimage}{subimagen}{subimágenes}
\Crefname{subimage}{Subimagen}{Subimágenes}

\crefname{subtable}{subtabla}{subtablas}
\Crefname{subtable}{Subtabla}{Subtablas}

\creflabelformat{equation}{#2#1#3}
\crefrangelabelformat{equation}{#3#1#4 to #5#2#6}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%                      INDEXES                         %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newcommand{\Index}[2][]%
{%
	\ifx&#1& #2\index{#2}%
	\else #2\index{#2|seealso{#1}}%
	\fi%
}%

\newcommand{\Subindex}[3][]%
{%
	\ifx&#1& #3\index{#2!#3}%
	\else #3\index{#2!#3|seealso{#1}}%
	\fi%
}%

\newcommand{\Subsubindex}[4][]%
{%
	\ifx&#1& #4\index{#2!#3!#4}%
	\else #4\index{#2!#3!#4|seealso{#1}}%
	\fi%
}%

\newcommand{\PhIndex}[2][]%
{%
	\ifx&#1& \index{#2}%
	\else \index{#2|seealso{#1}}%
	\fi%
}%

\newcommand{\PhSubindex}[3][]%
{%
	\ifx&#1& \index{#2!#3}%
	\else \index{#2!#3|seealso{#1}}%
	\fi%
}%

\newcommand{\PhSubsubindex}[4][]%
{%
	\ifx&#1& \index{#2!#3!#4}%
	\else \index{#2!#3!#4|seealso{#1}}%
	\fi%
}%

\newcommand{\newdefinition}[4]
{
	\ifx&#3&
		\newglossaryentry{#1}{name={#2},description={#4}}
	\else
		\newglossaryentry{#1}{name={#2},plural={#3},description={#4}}
	\fi
}

\def\dfn#1{\glsenablehyper\gls{#1}}
\def\dfnpl#1{\glsenablehyper\glspl{#1}}
\def\Dfn#1{\glsenablehyper\Gls{#1}}
\def\Dfnpl#1{\glsenablehyper\Dlspl{#1}}

\let\oldac\ac
\renewcommand{\ac}[1]%
{%
	\glsenablehyper\oldac{#1}%
}%

\newcommand{\mylistof}[2]
{
	\mysection*{#1}

		\txtfont
		\@cfttocstart
			\begingroup
				\parskip=0\myem
				\if@cfttocbibind
					\@cftdobiblof
				\fi
				\@namedef{l@lstlisting}{\@dottedtocline{1}{4\myex}{2.8\myem}}
				\@starttoc{#2}
			\endgroup
		\@cfttocfinish
}

\def\listoflists
{
	\if@listofalgsbool \listofalgorithms{\@auxvaralgorithmindex}  \fi
	\if@listofcodesbool \mylistof{\@auxvarcodeindex}{lol}  \fi
	\if@languagespa \if@listoftextboxesbool \listoftextboxes{\@auxvartextboxindex} \fi \fi
	\if@listofequationsbool \mylistof{\listequationname}{loe} \fi
	\if@listoffiguresbool \mylistof{\listfigurename}{lof} \fi
	\if@listoftablesbool \mylistof{\listtablename}{lot} \fi
	\if@languagespa \else \if@listoftextboxesbool \listoftextboxes{\@auxvartextboxindex} \fi \fi
}

\newcommand{\listoftextboxes}[1]
{
	\mysection*{#1}
	\txtfont
	\begingroup
		\setlength{\parskip}{\z@}
		\@namedef{l@textboxb}{\@dottedtocline{1}{4\myex}{2.8\myem}}
		\@starttoc{\@nameuse{ext@textboxb}}
	\endgroup
}

\newcommand{\listofalgorithms}[1]
{
	\mysection*{#1}
	\txtfont
	\begingroup
		\setlength{\parskip}{\z@}
		\@namedef{l@algorithmb}{\@dottedtocline{1}{4\myex}{2.8\myem}}
		\@starttoc{\@nameuse{ext@algorithmb}}
	\endgroup
}


\def\listoflists
{
	\if@nonelistbool\empty\else
		\if@alllistsbool
			\@newschapter{\@ListsChapter}
			\listofalgorithms{\@auxvaralgorithmindex}
			\mylistof{\@auxvarcodeindex}{lol}
			\if@languagespa \listoftextboxes{\@auxvartextboxindex} \fi
	    \mylistof{\listequationname}{loe}
			\mylistof{\listfigurename}{lof}
			\mylistof{\listtablename}{lot}
			\if@languagespa  \listoftextboxes{\@auxvartextboxindex} \fi
		\else
			\@newschapter{\@ListsChapter}
			\if@algorithmsbool \listofalgorithms{\@auxvaralgorithmindex} \fi
			\if@codesbool \mylistof{\@auxvarcodeindex}{lol} \fi
			\if@languagespa \else \if@textboxesbool \listoftextboxes{\@auxvartextboxindex} \fi \fi
			\if@equationsbool \mylistof{\listequationname}{loe} \fi
			\if@figuresbool \mylistof{\listfigurename}{lof} \fi
			\if@tablesbool \mylistof{\listtablename}{lot} \fi
			\if@languagespa \else \if@textboxesbool  \listoftextboxes{\@auxvartextboxindex} \fi \fi
		\fi
	\fi
}

















%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%                       COVERS                         %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%                                                  %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%                                              %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



\def\setnewlength#1#2
{
	 \newlength{#1}
	 \setlength{#1}{#2}
}

\setnewlength{\@orx}{-1in-1mm}
\setnewlength{\@ory}{-\paperheight+1in}
\setnewlength{\@qw}{0.25\paperwidth}
\setnewlength{\@bw}{0.065\paperwidth}
\setnewlength{\@sbw}{0.028\paperwidth}
\setnewlength{\@tbw}{0.001\paperwidth}
\setnewlength{\@sw}{0.34\paperwidth}
\setnewlength{\@pxo}{\@orx+\paperwidth-\@bw}
\setnewlength{\@pyt}{\@ory+\@bw}
\setnewlength{\@pyth}{\@ory+\paperheight-0.1667\paperwidth-1.5\@sbw}
\setnewlength{\@pyf}{\@ory+\paperheight-0.1667\paperwidth-2.5\@sbw}
\setnewlength{\@pyfv}{\@ory+\paperheight-0.1667\paperwidth-2.5\@sbw-4\@tbw}
\setnewlength{\@pxs}{\@orx+\paperwidth-\@sw-\@bw}
\setnewlength{\@pys}{\@ory+\paperheight-\@sw}
\setnewlength{\@pxsi}{\@orx+\paperwidth-0.925\@sw-\@bw}
\setnewlength{\@pysi}{\@ory+\paperheight-0.7\@sw}
\setnewlength{\@pwsi}{0.85\@sw}
\setnewlength{\@excpx}{\@orx+\@bw}
\setnewlength{\@excpy}{\@ory+1.5\@bw}
\setnewlength{\@excw}{0.2\paperwidth}
\setnewlength{\@posg}{\@ory+4\@bw}

\setnewlength{\@imgx}{\@orx+\@bw}
\setnewlength{\@imgy}{\@ory+4\@bw}
\setnewlength{\@imgw}{0.8\paperwidth}

\setnewlength{\@pxe}{\@orx+\@qw}
\setnewlength{\@pye}{\@ory+\paperheight-3\@qw}
\setnewlength{\@pyes}{\@ory+\paperheight-\@bw}
\setnewlength{\@pxei}{\@orx+1.15\@qw}
\setnewlength{\@pyei}{\@ory+\paperheight-2.45\@qw}
\setnewlength{\@pwei}{1.7\@qw}

\setnewlength{\@posxt}{\@orx+\@bw}
\setnewlength{\@posyt}{\@ory+\paperheight-1.72\@qw}
\setnewlength{\@posytt}{\@ory+\paperheight-0.1667\paperwidth-4\@sbw}
\setnewlength{\@posyttt}{\@ory+\paperheight-0.53\paperwidth}
\setnewlength{\@poswttt}{\paperwidth-2\@bw}
\setnewlength{\@posyuam}{\@ory+0.37\@bw}

\setnewlength{\@posxwww}{\@orx+\paperwidth-0.8\@bw}
\setnewlength{\@posywww}{\@ory+2\@bw}

\setnewlength{\@pxdata}{\@orx+\paperwidth-10\@bw-\@sbw}
\setnewlength{\@pydata}{\@ory+3\@bw}

\newcommand\nextyear{\advance\year by -1999 \the\year\advance\year by 1999}
\newcommand\prevyear{\advance\year by -2001 \the\year\advance\year by 2001}
\newcommand\actualyear{\advance\year by -2000 \the\year\advance\year by 2000}

\def\course
{
	\ifnum\month<8
	  \begin{center}\mbox{}\\[2.5\@sbw]\prevyear\\[-0.037\paperwidth]\rule{0.5\textwidth}{0.002\paperheight}\\[-0.02\paperwidth]\actualyear\end{center}
	\else
	  \begin{center}\mbox{}\\[2.5\@sbw]\actualyear\\[-0.037\paperwidth]\rule{0.5\textwidth}{0.002\paperheight}\\[-0.02\paperwidth]\nextyear\end{center}
	\fi
}


\def\mycoloredbox#1#2#3#4#5
{
	\fancyput*(0in,0in){}
	\thisfancyput*(#1,#2)
	{
		\setlength{\fboxsep}{0pt}\colorbox{#5}{\hbox to #3 {\vbox to #4{\mbox{}}}}
	}
}

\def\textpos#1#2#3#4#5
{
	\fancyput*(0in,0in){}
	\thisfancyput*(#1,#2){\color{#3} #4 #5}
}

\def\minipagetextpos#1#2#3#4#5#6
{
	\fancyput*(0in,0in){}
	\thisfancyput*(#1,#2)
	{
		\begin{minipage}{#3}
			\color{#4} #5 #6
		\end{minipage}
	}
}

\def\imagepos#1#2#3#4
{
	\fancyput*(0in,0in){}
	\thisfancyput*(#1,#2)
	{
		\logopgfimage[width=#3]{#4}
	}
}

\def\covertitle
{
	\fancyput*(0in,0in){}
	\thisfancyput*(\@posxt,\@posyt)
	{
		\color{uamgray} \coverfont
		\if@tfgwork	\if@languagespa Trabajo fin de grado \else Bachelor thesis \fi \fi
		\if@tfmwork \if@languagespa Trabajo fin de máster \else Master thesis \fi \fi
		\if@thesiswork \if@languagespa Tesis \else Thesis \fi \fi
	}
}

\def\coverimage
{
	\if@epsbool \imagepos{\@imgx}{\@imgy}{\@imgw}{epsfoto} \fi
	\if@cienciasbool \imagepos{\@imgx}{\@imgy}{\@imgw}{cienciasfoto} \fi
	\if@medicinabool \imagepos{\@imgx}{\@imgy}{\@imgw}{medicinafoto} \fi
	\if@enfermeriabool \imagepos{\@imgx}{\@imgy}{\@imgw}{medicinafoto} \fi
	\if@fisioterapiabool \imagepos{\@imgx}{\@imgy}{\@imgw}{medicinafoto} \fi
	\if@psicologiabool \imagepos{\@imgx}{\@imgy}{\@imgw}{psicologiafoto} \fi
	\if@filosofiabool \imagepos{\@imgx}{\@imgy}{\@imgw}{filosofiafoto} \fi
	\if@profesoradobool \imagepos{\@imgx}{\@imgy}{\@imgw}{profesoradofoto} \fi
	\if@derechobool \imagepos{\@imgx}{\@imgy}{\@imgw}{derechofoto} \fi
	\if@economicasbool \imagepos{\@imgx}{\@imgy}{\@imgw}{economicasfoto} \fi
}

\def\coverpage
{
	\cleardoublepage
	\pagestyle{empty}
	\fancyhf{}

	\mycoloredbox{\@pxo}{\@ory}{\@bw}{\paperheight}{maincolor}
	\mycoloredbox{\@orx}{\@ory}{\paperwidth}{\@bw}{uambased}
	\mycoloredbox{\@orx}{\@pyth}{\paperwidth}{\@sbw}{uambased}
	\mycoloredbox{\@orx}{\@pyf}{\paperwidth}{\@sbw}{uamgray}
	\mycoloredbox{\@orx}{\@pyfv}{\paperwidth}{\@tbw}{uambased}
	\mycoloredbox{\@pxs}{\@pys}{\@sw}{\@sw}{uambased}
	\imagepos{\@pxsi}{\@pysi}{\@pwsi}{logoUAMw}
	\imagepos{\@excpx}{\@excpy}{\@excw}{campusEx}
	\mycoloredbox{\@orx}{\@posg}{0.667\paperwidth}{0.4\paperheight}{vluamgray}
	\coverimage
	\covertitle
	\textpos{\@posxt}{\@posytt}{black}{\textbf\txtfont}{\@faculty}
	\minipagetextpos{\@posxt}{\@posyttt}{\@poswttt}{maincolor}{\LARGE\textbf\txtfont}{\@titleaux}
	\minipagetextpos{\@orx}{\@posyuam}{\paperwidth}{white}{\LARGE\begin{center}Universidad Autónoma de Madrid\end{center}}
	\textpos{\@posxwww}{\@posywww}{white}{\wwwfont}{\rotatebox{90}{www.uam.es}}
	\minipagetextpos{\@pxo}{\@orx}{\@bw}{white}{\LARGE\textbf\txtfont}{\course}
	\minipagetextpos{\@pxdata}{\@pydata}{9\@bw}{black}{\LARGE\textbf\txtfont}{\flushright{\color{maincolor}\noindent\large\@author}\\[0.01\paperheight]\footnotesize\@auxcoverdata}
}

\def\endcoverpage
{
	\clearsdoublepage
	\pagestyle{empty}
	\mbox{}
	\newpage
	\mbox{}
	\mycoloredbox{\@orx}{\@ory}{\paperwidth}{\@bw}{uambased}
	\mycoloredbox{\@pxe}{\@pye}{2\@qw}{2\@qw}{uambased}
	\mycoloredbox{\@orx}{\@pyes}{\paperwidth}{\@bw}{uamgray}
	\imagepos{\@pxei}{\@pyei}{\@pwei}{logoUAMw}
}

\def\leveltext
{
	\if@languagespa
		\if@tfgwork
			\begin{center}\begin{large}\textbf{Grado en \@levelin}\end{large}\end{center}	
		\else
			\if@tfmwork
				\begin{center}\begin{large}\textbf{Máster en \@levelin}\end{large}\end{center}
			\else
				\begin{center}\begin{large}\textbf{Doctor en \@levelin}\end{large}\end{center}
			\fi
		\fi
	
	\else
		\if@tfgwork
			\begin{center}\begin{large}\textbf{Bachelor as \@levelin}\end{large}\end{center}	
		\else
			\if@tfmwork
				\begin{center}\begin{large}\textbf{Master as \@levelin}\end{large}\end{center}
			\else
				\begin{center}\begin{large}\textbf{PhD. as \@levelin}\end{large}\end{center}
			\fi
		\fi
	\fi
}

\def\worktext
{
	\if@languagespa
		\if@tfgwork
			\begin{center}\begin{huge} \textbf{TRABAJO FIN DE GRADO} \end{huge}\end{center}
		\else
			\if@tfmwork
				\begin{center}\begin{huge} \textbf{TRABAJO FIN DE MÁSTER} \end{huge}\end{center}
			\else
				\begin{center}\begin{huge} \textbf{TESIS} \end{huge}\end{center}
			\fi
		\fi
	\else
		\if@tfgwork
			\begin{center}\begin{huge} \textbf{BACHELOR THESIS} \end{huge}\end{center}
		\else
			\if@tfmwork
				\begin{center}\begin{huge} \textbf{MASTER THESIS} \end{huge}\end{center}
			\else
				\begin{center}\begin{huge} \textbf{PHD. THESIS} \end{huge}\end{center}
			\fi
		\fi
	\fi
}

\def\titlepage
{
	\cleardoublepage
	\pagestyle{empty}

	\setlength{\exposa}{0.22\paperwidth-1in}
	\setlength{\exposc}{0.715\paperwidth-1in}
	\fancyhf{}
	\if@finalmodebool \else
		\setlength{\exposb}{0.1\paperwidth-1in}
		\fancyput*(0in,0in){}
		\thisfancyput*(-0.05\exposb,-0.84\paperheight){\rotatebox{62}{\scalebox{5.5}{\color{draftcolor} \txtchapfont DRAFT}}}
		\fancyput*(-0.05\exposb,-0.84\paperheight){\rotatebox{62}{\scalebox{5.5}{\color{draftcolor} \txtchapfont DRAFT}}}
	\fi

	\newdateformat{tfgdate}{\monthname[\THEMONTH] \THEYEAR}

	\def\loctitlefont{\fontsize{12}{14} \usefont{T1}{pxr}{b}{n}\selectfont}
	\loctitlefont
	\if@languagespa
		\vspace*{0.15\textheight}
		\@auxuniversityfaculty
		\vspace*{0.05\textheight}
		\hfill
		\logopgfimage[height=0.08\textheight]{\@facultylogo}
		\hspace*{0.005\textwidth}
		\logopgfimage[height=0.08\textheight]{logoUAM}
		\hfill
		\vspace*{0.05\textheight}
		\leveltext
		\vspace*{0.02\textheight}
		\worktext
		\vspace*{0.02\textheight}
		\begin{center}
			\begin{minipage}{0.7\textwidth}
				\begin{center}\begin{Large}\textbf{\@titleaux}\end{Large}\end{center}
				\if@subtitlebool \begin{center}\begin{large}\textbf{\@subtitleaux}\end{large}\end{center} \fi
			\end{minipage}
		\end{center}
		\vfill
		\begin{center}
			Autor: \@author \\ \mbox{}
			Tutor: \@advisor \\ \mbox{}
			\if@coadvisorbool Cotutor: \@coadvisor \\ \mbox{}\fi
			\ifx\@speaker\empty\else
				Ponente: \@speaker \\[1\myem]
			\fi
			\vspace*{0.02\textheight}
			\begin{center}\tfgdate\today \end{center}
		\end{center}
	\else
		\vspace*{0.15\textheight}
		\@auxuniversityfaculty
		\vspace*{0.05\textheight}
		\hfill
		\logopgfimage[height=0.08\textheight]{\@facultylogo}
		\hspace*{0.005\textwidth}
		\logopgfimage[height=0.08\textheight]{logoUAM}
		\hfill
		\vspace*{0.05\textheight}
		\leveltext
		\vspace*{0.02\textheight}
		\worktext
		\vspace*{0.02\textheight}
		\begin{center}
			\begin{minipage}{0.7\textwidth}
				\begin{center}\begin{Large}\textbf{\@titleaux}\end{Large}\end{center}
				\if@subtitlebool \begin{center}\begin{large}\textbf{\@subtitleaux}\end{large}\end{center} \fi
			\end{minipage}
		\end{center}
		\vfill
		\begin{center}
			Author: \@author \\ \mbox{}
			Advisor: \@advisor \\ \mbox{}
			\if@coadvisorbool Coadvisor: \@coadvisor \\ \mbox{}\fi
			\ifx\@speaker\empty\else
				Ponente: \@speaker \\[1\myem]
			\fi
			\vspace*{0.02\textheight}
			\begin{center}\tfgdate\today \end{center}
		\end{center}
	\fi

	\newpage
	\txtcopyrightfont
	\begin{footnotesize}
		\mbox{}
		\vfill
		\vbox{
			\allrightsreserved
			\printedon
		}
	\end{footnotesize}
	\newpage
}

\begin{filecontents}{\jobname.ist}
	headings_flag 1

	heading_prefix "\n\\centering{\\large\\color\{maincolor\}\\bfseries%
	\\noindent\\textbf{--- "
	heading_suffix " ---}}\\par\\nopagebreak\n"

	delim_0 "\\dotfill "
	delim_1 "\\dotfill "
	delim_2 "\\dotfill "
	delim_r "\\textendash"
	suffix_2p "\\nohyperpage{\\,f.}"
	suffix_3p "\\nohyperpage{\\,ff.}"
	page_compositor "."
	item_0 "\n \\item \\small "
\end{filecontents}

\makeindex
\makeglossaries

\if@fullindexbool	\setcounter{tocdepth}{3}
\else
 	\if@extendedindexbool \setcounter{tocdepth}{2}
	\else \setcounter{tocdepth}{1}
	\fi
\fi


\AtBeginDocument
{
	\setnames
	\if@coversbool \coverpage \fi
	\titlepage

	\renewcommand{\thepage}{\roman{page}}
	\txtfont
	\ifx\@dedication\empty
		\ifx\@famouscite\empty
			\empty
		\else
			\newpage
			\begin{flushright}
				\textit{\@famouscite}
			\end{flushright}
		\fi
	\else
		\ifx\@famouscite\empty
			\newpage
			\begin{flushright}
				\textit{\@dedication}
			\end{flushright}
		\else
			\newpage
			\begin{flushright}
				\textit{\@dedication}
			\end{flushright}
			\vspace{0.2\paperheight}
			\begin{flushright}
				\textit{\@famouscite}
			\end{flushright}
		\fi
	\fi

	\pretexts
	\cleardoublepage
	\@schapter{\contentsname}
	\@starttoc{toc}
	\listoflists
}

\AtEndDocument
{
	\if@appendixbool\else
		\thesisbibliography
		\printglossaries
	\fi
	\cleardoublepage
	\pagestyle{indexst}
	\printindex
	\if@coversbool \endcoverpage \fi
}

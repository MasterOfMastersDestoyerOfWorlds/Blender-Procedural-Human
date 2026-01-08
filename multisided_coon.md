\documentclass{article}

\usepackage[utf8]{inputenc}
\usepackage{amsmath, amssymb, amsfonts}
\usepackage{graphicx}
\usepackage{geometry}
\usepackage{hyperref}
\usepackage{url}

% Setup geometry
\geometry{a4paper, margin=1in}

% Title and Author
\title{A multi-sided generalization of the $C^0$ Coons patch}
\author{Péter Salvi \\
\small Budapest University of Technology and Economics \\
\small \texttt{salvi@iit.bme.hu}}
\date{February 26, 2020}

\begin{document}

\maketitle

\begin{abstract}
Most multi-sided transfinite surfaces require cross-derivatives at the boundaries. Here we show a general $n$-sided patch that interpolates all boundaries based on only positional information. The surface is a weighted sum of $n$ Coons patches, using a parameterization based on Wachspress coordinates.
\end{abstract}

\section{Introduction}
Filling an $n$-sided hole with a multi-sided surface is an important problem in Computer Aided Geometric Design (CAGD). Usually, the patch should connect to the adjacent surfaces with at least $G^1$ continuity, but in some applications only positional ($C^0$) continuity is needed, and normal vectors or cross derivatives at the boundary curves are not available. For $n = 4$, the $C^0$ Coons patch solves this problem; in this paper, we show how to generalize it to any number of sides.

\section{Previous Work}
Most transfinite surface representations in the literature assume $G^1$ constraints, and the patch equations make use of the fixed cross-derivatives at the boundary. This can be circumvented by generating a normal fence automatically, e.g., with a rotation minimizing frame; however, in a $C^0$ setting this is an overkill, and simpler methods exist.

One well-known solution is the harmonic surface, which creates a ``soap film'' filling the boundary loop by solving the harmonic equation on a mesh with fixed boundaries. This, however, minimizes the total area of the surface, which often has unintuitive results (see Section 4). The basic idea of the proposed method, i.e., to define the surface as the weighted sum of $n$ Coons patches, each interpolating three consecutive sides, is the same as in the CR patch.

\section{The multi-sided $C^0$ Coons patch}
Let $C_i(t) : [0, 1] \to \mathbb{R}^3$ denote the $i$-th boundary curve. Let us also assume $C_i(1) = C_{i+1}(0)$ for all $i$ (using circular indexing). Then the ribbon $R_i$ is defined as a $C^0$ Coons patch interpolating $C_{i-1}$, $C_i$, $C_{i+1}$, and $C^{opp}_i$.

The ribbon is a cubic curve fitted onto the initial and (negated) end derivatives of sides $i+2$ and $i-2$, respectively. Formally, the ribbon equation is given by:

\begin{equation}
\begin{split}
R_i(s_i, d_i) = \;& (1 - d_i)C_i(s_i) + d_i C^{opp}_i(1 - s_i) \\
&+ (1 - s_i)C_{i-1}(1 - d_i) + s_i C_{i+1}(d_i) \\
&- \left[ (1-s_i)(1-d_i)C_i(0) + s_i(1-d_i)C_i(1) \right. \\
&\quad \left. + (1-s_i)d_i C^{opp}_i(1) + s_i d_i C^{opp}_i(0) \right]
\end{split}
\end{equation}

where $C^{opp}_i$ is defined as the Bézier curve determined by the control points $P_0, P_1, P_2, P_3$:

\begin{align}
P_0 &= C_{i+1}(1) \\
P_1 &= P_0 + \frac{1}{3} \mathbf{v}_{i+2}^{start} \\
P_2 &= P_3 - \frac{1}{3} \mathbf{v}_{i-2}^{end} \\
P_3 &= C_{i-1}(0)
\end{align}

Here, $\mathbf{v}_{k}^{start}$ and $\mathbf{v}_{k}^{end}$ denote the tangent (or chordal) vectors derived from the adjacent sides $i+2$ and $i-2$.

\subsection{Parameterization}
The surface is defined over a regular $n$-sided polygon. The Wachspress coordinates of a domain point $p$ are defined as:

\begin{equation}
\lambda_i = \lambda_i(p) = \frac{\prod_{j \neq i-1, i} D_j(p)}{\sum_{k=1}^n \prod_{j \neq k-1, k} D_j(p)}
\end{equation}

where $D_i(p)$ is the perpendicular distance of $p$ from the $i$-th edge of the domain polygon. Ribbon parameterization is based on these generalized barycentric coordinates:

\begin{equation}
d_i = d_i(u, v) = 1 - \lambda_{i-1} - \lambda_i, \quad s_i = s_i(u, v) = \frac{\lambda_i}{\lambda_{i-1} + \lambda_i}
\end{equation}

It is easy to see that $s_i, d_i \in [0, 1]$, and that $d_i$ has the following properties:
\begin{enumerate}
    \item $d_i = 0$ on the $i$-th side.
    \item $d_i = 1$ on the ``far'' sides (all sides except $i-1$, $i$, and $i+1$).
    \item $d_{i-1} + d_{i+1} = 1$ on the $i$-th side.
\end{enumerate}

\subsection{Surface Definition}
Finally, we define the patch as:

\begin{equation}
S(p) = \sum_{i=1}^n R_i(s_i, d_i) B_i(d_i)
\end{equation}

where $B_i$ is the blending function:

\begin{equation}
B_i(d_i) = (1 - d_i)^2
\end{equation}

The interpolation property is satisfied due to the properties of $d_i$ mentioned above. Note that $s_i$ in Eq. (5) cannot be evaluated when $d_i = 1$, but at these locations the weight $B_i(d_i)$ also vanishes.

\section{Examples}
Comparison with the harmonic surface shows that the proposed method avoids the unnaturally flat patches resulting from the area-minimizing property of harmonic functions. The mean curvature map and contouring show good surface quality.

\section{Conclusion}
We have defined a natural generalization of the $C^0$ Coons patch -- a lightweight and efficient multi-sided surface representation, applicable when only positional data is available.

\section*{Acknowledgements}
This work was supported by the Hungarian Scientific Research Fund (OTKA).

\end{document}
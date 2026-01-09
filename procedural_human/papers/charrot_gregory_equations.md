# Multi-sided surfaces interpolating arbitrary boundaries with intuitive interior control

**Péter Salvi**

## Motivation

Multi-sided patches usually either have arbitrary boundary constraints (transfinite interpolation surfaces) or natural interior control (generalized Bézier patches), but not both - until now! The goal is to find a surface representation that fits those boundaries and potentially prescribed tangential information while maintaining intuitive interior control.

## Outline

* Motivation
* Transfinite interpolation surfaces
* Katō's patch
* Charrot–Gregory patch


* Midpoint patch
* Hybrid patch
* Conclusion

## Transfinite interpolation surfaces

Existing transfinite interpolation methods like **Katō's patch** and the **Charrot-Gregory patch** excel at interpolating arbitrary boundary constraints (position and cross-derivatives) but lack intuitive interior control.

## Hybrid Patch

The proposed **Hybrid Patch** effectively integrates both ribbon-based (transfinite) and control-based surfaces, inheriting the advantages of each.

* **Key Advantage:** It can handle positional and cross-derivative boundary constraints of arbitrary degrees while providing fine-grained control of the interior.
* **Construction:**
* It uses blending functions based on Hermite blends.
* 
* 
α0​(x)=1
α1​(x)=2x3−3x2+1

 (Hermite blends)
* The construction involves terms like:

di−1​α0​(si​)α0​(di​)+di​α1​(si−1​)α0​(di−1​)

* **Weight deficient  extra DoF**: The weight deficiency in the basis functions allows for extra degrees of freedom, which are utilized for shape control.



## Conclusion

The hybrid patch represents an improvement over Katō's patch by incorporating interior control and is more versatile than generalized Bézier surfaces as it supports arbitrary boundary constraints.

Based on the uploaded slides, here are the specific equations for the Charrot–Gregory patch and the Hybrid patch.

### 1. Charrot–Gregory Patch (CAGD, 1984)

This slide outlines the corner interpolant construction, which approximates a partial Coons patch.

* **Surface Equation:**

S=i∑​Ri−1,i​Li−1,i​
* **Corner Interpolant:**
Ri−1,i​=Ri−1​+Ri​−Qi−1,i​


*(Note:  and  typically refer to the ribbon interpolants derived from the sides, and  is the corner correction term)*
* **Weight Function (Rational Blend):**
Li−1,i​=∑j​∏k∈/{j,j−1}​dk2​∏k∈/{i,i−1}​dk2​​


*(Note:  represents the distance to the -th side)*

### 2. Hybrid Patch

This slide presents the unified equation for the Hybrid patch, which combines control points () with ribbon interpolants ().

* **Surface Equation:**

Surface Equation:
S(u,v)=i=1∑n​​j=0∑p​k=2∑⌊2p−1​⌋​Ci,j,k​⋅μi,j,k​Bjp​(si​)Bkp​(di​)+Ri​(si​,di​)⋅similar to Li​(d1​,...,dn​)j=0∑p​k=0∑1​μi,j,k​Bjp​(si​)Bkp​(di​)​​​+C0​BΣ​(u,v)


Ci,j,k​: Interior control points.

Ri​(si​,di​): The boundary ribbon interpolant.

Bjp​: Bernstein polynomials of degree p.

μi,j,k​: Weight functions.

k=2 in the first sum: This indicates that the control points start influencing the surface from the second "layer" inwards, leaving the boundary layers (k=0,1) to be defined by the ribbon Ri​.

C0​BΣ​(u,v): The central control point term.


A multi-sided generalization
of the C0 Coons patch
P´eter Salvi
Budapest University of Technology and Economics
February 27, 2020
Abstract
Most multi-sided transfinite surfaces require cross-derivatives at the
boundaries. Here we show a general n-sided patch that interpolates
all boundaries based on only positional information. The surface is a
weighted sum of n Coons patches, using a parameterization based on
Wachspress coordinates.
1 Introduction
Filling an n-sided hole with a multi-sided surface is an important problem in
CAGD. Usually the patch should connect to the adjacent surfaces with at least
G1 continuity, but in some applications only positional (C0) continuity is needed,
and normal vectors or cross derivatives at the boundary curves are not available.
For n = 4, the C0 Coons patch [1] solves this problem; in this paper we show
how to generalize it to any number of sides.
2 Previous work
Most transfinite surface representation in the literature assume G1 constraints,
and the patch equations make use of the fixed cross-derivatives at the boundary.
This can be circumvented by generating a normal fence automatically, e.g. with
a rotation minimizing frame [3]; however, in a C0 setting this is an overkill,
simpler methods exist.
One well-known solution is the harmonic surface, which creates a “soap film”
filling the boundary loop by solving the harmonic equation on a mesh with fixed
boundaries. This, however, minimizes the total area of the surface, which often
has unintuitive results, see an example in Section 4.
The basic idea of the proposed method, i.e., to define the surface as the
weighted sum of n Coons patches, each interpolating three consecutive sides, is
the same as in the CR patch [2].
1
arXiv:2002.11347v1 [cs.GR] 26 Feb 2020
i
i+1
i+2
i-1
i-2Figure 1: Construction of a four-sided Coons ribbon.
3 The multi-sided C0 Coons patch
Let Ci(t) : [0, 1] → R3 denote the i-th boundary curve. Let us also assume
Ci(1) = Ci+1(0) for all i (with circular indexing). Then the ribbon Ri is defined
as a C0 Coons patch interpolating Ci−1, Ci, Ci+1, and Copp
i – a cubic curve
fitted onto the initial and (negated) end derivatives of sides i + 2 and i − 2,
respectively (see Figure 1).
Formally,
Ri(si, di) = (1 − di)Ci(si) + diCopp
i (1 − si)
+ (1 − si)Ci−1(1 − di) + siCi+1(di)
−
[ 1 − si
si
]ᵀ [ Ci(0) Ci−1(0)
Ci(1) Ci+1(1)
] [ 1 − di
di
]
, (1)
where Copp is defined as the B´ezier curve1 determined by the control points
P0 = Ci+1(1), P1 = P0 + 1
3 C′
i+2(0), (2)
P2 = P3 − 1
3 C′
i−2(1), P3 = Ci−1(0). (3)
The surface is defined over a regular n-sided polygon. The Wachspress co-
ordinates of a domain point p are defined as
λi = λi(p) =
∏
j6 =i−1,i Dj (p)
∑n
k=1
∏
j6 =k−1,k Dj (p) , (4)
where Di(p) is the perpendicular distance of p from the i-th edge of the domain
polygon. Ribbon parameterization is based on these generalized barycentric
coordinates:
di = di(u, v) = 1 − λi−1 − λi, si = si(u, v) = λi
λi−1 + λi
. (5)
It is easy to see that si, di ∈ [0, 1], and that di has the following properties:
1Except for n = 3, where Copp degenerates to the point Ci+1(1).
2
(a) Harmonic surface (b) C0 Coons patch
(c) Harmonic surface (contours) (d) C0 Coons patch (contours)
Figure 2: Comparison with the harmonic surface on a 5-sided boundary loop.
1. di = 0 on the i-th side.
2. di = 1 on the “far” sides (all sides except i − 1, i and i + 1).
3. di−1 + di+1 = 1 on the i-th side.
Finally, we define the patch as
S(p) =
n∑
i=1
Ri(si, di)Bi(di), (6)
where Bi is the blending function
Bi(di) = 1 − di
2 . (7)
The interpolation property is satisfied due to the properties of di mentioned
above.
(Note: si in Eq. (5) cannot be evaluated when di = 1, but at these locations
the weight Bi(di) also vanishes.)
4 Examples
Figure 2 shows a comparison with the harmonic surface, which – due to its area
minimizing property – results in an unnaturally flat patch.
Figure 3 shows a model with 5 patches: two 3-sided, one 4-sided, one 5-
sided, and one 6-sided. The mean curvature map and contouring both show
good surface quality.
3
(a) Mean curvature map (b) Contouring
Figure 3: The “pocket” model.
Conclusion
We have defined a natural generalization of the C0 Coons patch – a lightweight
and efficient multi-sided surface representation, applicable when only positional
data is available.
Acknowledgements
This work was supported by the Hungarian Scientific Research Fund (OTKA,
No. 124727).
References
[1] Steven Anson Coons. Surfaces for computer-aided design of space forms.
Technical Report MIT/LCS/TR-41, Massachusetts Institute of Technology,
1967.
[2] P´eter Salvi, Tam´as V´arady, and Alyn Rockwood. Ribbon-based transfinite
surfaces. Computer Aided Geometric Design, 31(9):613–630, 2014.
[3] Wenping Wang, Bert J¨uttler, Dayue Zheng, and Yang Liu. Computation of
rotation minimizing frames. ACM Transactions on Graphics, 27(1):2, 2008
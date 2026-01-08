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
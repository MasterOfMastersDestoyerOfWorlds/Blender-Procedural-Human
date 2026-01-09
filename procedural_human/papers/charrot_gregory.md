# Charrot Gregory Patch

Makogan | Demiurge 

This explains how to construct a Charrot-Gregory patch, which is a generalization of a Coons patch. It blends multiple curves together into a unified, smooth surface, and also takes into account bitangent information.

## Contents

1. Motivation 


2. Charrot Gregory Patch 2.1 Note 2.2 Inputs 2.3 Weights 2.4 Sample points 2.5  Patch 2.6  Patch 


3. Closing thoughts Bibliography 



---

## 1. Motivation

Sometimes you have a set of curves which are meant to describe the boundary of a surface and you want to find a surface that fits those boundaries and potentially prescribed tangential information. This algorithm does just that.

*Figure 1: Surfaces obtained by blending three, four, five and six curves, respectively.* 

---

## 2. Charrot Gregory Patch

### 2.1 Note

This document heavily deviates from the original paper in terms of notation, despite describing the same process. It also explains it in a more general way to apply to more shapes. Also, all index notation is modular so e.g.  when  is the same as .

### 2.2 Inputs

The input to the method will be  curves in  such that they are attached at their endpoints, forming a closed, piecewise smooth curve, and an optional set of prescribed bitangents at each of these curves. The output will be a surface that blends all such points together, is smooth, and, optionally, matches the prescribed bitangents.

### 2.3 Weights

In order to produce the final surface we will need a set of blending weights and a set of sampling points on the boundaries.

We start by generating a regular polygon  with  sides, that will be mapped to the output surface. Then assume we have a point  within the interior of the polygon that we wish to map to the surface.

We will first compute the orthogonal distance of  along the edge:




This will generate  positive scalar weights, as seen in Figure 2. To generate the weights we will iterate over every vertex, then we will define the function:



i.e. we will take the product of the orthogonal distances to all edges not incident on vertex , so in Figure 2 that would correspond to  when focusing on vertex .

*Figure 2: Orthogonal distances of a point to the edges of the polygon.* 

And then we must normalize the weights, thus:




### 2.4 Sample points

Now, for each corner of the polygon, we will generate a point to be blended using the above weights. First, we will generate two sampling weights:





And with these we will be able to define two points on the curves of the surface.





Where  is the -th curve in the input and we assume the curve has been parametrized as .

In case we also want tangent information, then we also produce the tangents:






### 2.5  Patch

If all we care about is producing a smooth surface that interpolates the boundary, then we can construct the surface as follows.

First construct an intermediary point:




Note that  by construction, and thus  when  is 0 and  when  is 0.

This allows us to create  distinct points which have the following properties:

* If  was on edge  of the polygon, then  is exactly on curve  of the input curves.


* If  was on the vertex of the polygon, then  is exactly on the vertex of  at which  and  meet.



Finally we compute our output surface point  as:




### 2.6  Patch

*Figure 3: Surfaces by modifying the prescribed tangents of a hexagonal patch.* 

If we also want to match the prescribed tangential information, then we must involve the tangents. In which case we modify the computation of  to be:



Where  are the prescribed tangents at the endpoints of the respective curves  at their shared endpoint. And  is a twist condition vector, in practice it can be set to 0.

---

## 3. Closing thoughts

This document focused on a very "get it done" approach to describe the method and glosses over any proofs as to why it works. The original paper [1] has many interesting derivations which are worth a read. Additionally [3] has a set of related papers which may be better suited to certain applications.

## Bibliography

1. P. Charrot and J. A. Gregory, "A pentagonal surface patch for computer aided geometric design," *Computer Aided Geometric Design*, vol. 1, no. 1, pp. 87-94, Jul. 1984, doi: 10.1016/0167-8396(84)90006-2. 


2. S. A. Coons, "Surfaces for Computer-aided Design of Space Forms," Jun. 1967, Accessed: Oct. 27, 2024. [Online]. Available: [https://dspace.mit.edu/handle/1721.1/149362](https://dspace.mit.edu/handle/1721.1/149362) 


3. P. Salvi, "Multi-sided generalizations of the Coons patch."
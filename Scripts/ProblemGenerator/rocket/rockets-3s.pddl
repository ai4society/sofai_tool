(define (problem rrt3s)
  (:domain rockets-s)
  (:requirements :strips)
  (:objects l1 l2 l3
			r1 r2 r3 r4
			c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12)
  (:init
   (location l1) (location l2) (location l3)
   (rocket r1) (rocket r2) (rocket r3) (rocket r4)
   (cargo c1) (cargo c2) (cargo c3) (cargo c4) (cargo c5) (cargo c6) (cargo c7) (cargo c8) (cargo c9) (cargo c10) (cargo c11) (cargo c12)
    
   (at r1 l1) (at r2 l1) (at r3 l1) (at r4 l1)
   (at c1 l1) (at c2 l2) (at c3 l3) (at c4 l3) (at c5 l2) (at c6 l1) (at c7 l1) (at c8 l2) (at c9 l3) (at c10 l1) (at c11 l2) (at c12 l3)
   )
  
   (:goal (and (at c2 l1) (at c3 l2) (at c1 l3) (at c4 l2) (at c5 l1) (at c6 l3) (at c7 l2) (at c8 l3) (at c9 l1) (at c10 l2) (at c11 l3) (at c12 l1)))
)

(define (problem problem_10_2)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10)
(:init 
(handempty)
(on b1 b5)
(on b2 b10)
(on b3 b7)
(on b4 b6)
(clear b4)
(ontable b5)
(on b6 b1)
(ontable b7)
(on b8 b3)
(clear b8)
(on b9 b2)
(clear b9)
(ontable b10)
)
(:goal
(and
(on b1 b9)
(on b2 b3)
(on b3 b4)
(ontable b4)
(on b5 b2)
(on b6 b10)
(clear b6)
(on b7 b1)
(ontable b8)
(clear b8)
(on b9 b5)
(on b10 b7)

)

)
)
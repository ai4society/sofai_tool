(define (problem problem_5_22)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5)
(:init 
(handempty)
(ontable b1)
(on b2 b1)
(on b3 b4)
(clear b3)
(on b4 b5)
(on b5 b2)
)
(:goal
(and
(on b1 b2)
(on b2 b5)
(on b3 b1)
(on b4 b3)
(clear b4)
(ontable b5)

)

)
)
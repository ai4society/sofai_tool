(define (problem problem_5_74)
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
(on b1 b3)
(clear b1)
(ontable b2)
(on b3 b4)
(on b4 b5)
(on b5 b2)

)

)
)
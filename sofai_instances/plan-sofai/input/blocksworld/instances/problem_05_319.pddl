(define (problem problem_5_319)
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
(on b1 b4)
(on b2 b1)
(ontable b3)
(on b4 b3)
(on b5 b2)
(clear b5)

)

)
)
import euclid
problem_point = euclid.Point2(1.0, 2.0)

problem_line = euclid.Line2(euclid.Point2(1.0, 0.0), euclid.Point2(2.0, 2.0))


print problem_line.distance(problem_point)


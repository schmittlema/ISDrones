import euclid
problem_point = euclid.Point2(0.0, 30.0)

problem_line = euclid.Line2(euclid.Point2(0.0, 0.0), euclid.Point2(0.0, 50.0))
problem_point.distance(problem_line)

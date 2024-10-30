(defun au9-power (b e)
  (expt b e))

(defun power (base exp)
  (cond ((= exp 0) 1)
	((evenp exp) (expt (power base (/ exp 2)) 2))
	(t (* base (power base (- exp 1))))))

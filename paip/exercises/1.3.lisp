(defun count-atoms (expression)
  (cond ((null expression) 0)
	((atom expression) 1)
	(t (+ (count-atoms (car expression))
	      (count-atoms (cdr expression))))))


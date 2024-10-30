(defun au9-dot-product (n1 n2)
  (apply #'+ (mapcar #'* n1 n2)))

(defun dot-product (a b)
  (apply #'+ (mapcar #'* a b)))
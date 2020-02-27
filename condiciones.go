package main

import "fmt"
/*
== igual a
!= diferente
< menor que
> mayor que
<= menor o igual que
>= mayor o igual que
&& AND
|| OR
*/

func main()  {
  x := 10
  y := 5
  if x > y {
    fmt.Printf("%d es mayor que %d\n", x, y)
  }
}

package main

import(
  "fmt"
  "bufio"
  "os"
)

func main()  {
  // Ingresar edad(INT) e imorimir resultado
  // var edad int
  // fmt.Println("Coloca tu edad: ")
  // fmt.Scanf("%d\n",&edad)
  // fmt.Printf("Mi edad es %d\n", edad)

  // Imprimir string
  // var nombre string
  // fmt.Println("Ingresa tu nombre: ")
  // fmt.Scanf("%s\n",&nombre)
  // fmt.Printf("Hola %s\n", nombre)

  //Otro metodo importando bufio y os
  reader := bufio.NewReader(os.Stdin)
  fmt.Println("Ingresa tu nombre: ")
  nombre,err := reader.ReadString('\n')
  if(err != nil){
    fmt.Println(err)
  }else{
    fmt.Println("Hola " + nombre)
  }
}

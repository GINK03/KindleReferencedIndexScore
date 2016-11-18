import scala.io.StdIn.readLine

object Main {
  def main(args: Array[String]){
    val nk  = readLine().split(" ").map(_.toInt)
    val (n, k) = (nk(0), nk(1))
    if (n == k ) {
      println("Drew")
      return 
    }
    if ( (n, k) == (0, 1) || (n, k) == (1, 2) || (n, k) == (2, 0 ) )  {
      println("Won")
      return 
    }
    if ( (n, k) == (1, 0) || (n, k) == (2, 1) || (n, k) == (0, 2 ) )  {
      println("Lost")
      return 
    }
  }
}

import scala.io.StdIn.readLine
import scala.collection.immutable.StringLike
import scala.collection.immutable.Stream
import Math.{sqrt, pow}
import scala.util.control.Breaks

object Main {
  val inf = Stream.continually(List(None, None, Some("Fizz")).toStream).flatten
  val inf2 = Stream.from(1)
  val inf3 = Stream.continually(1)
  val _lmax  = Long.MaxValue
  val _imax  = Int.MaxValue
  val b1   = new Breaks
  def main(args: Array[String]){
    val is = readLine().toInt
    val gds = (1 to is).map { x =>
      val is2 = readLine().split(" ").map { x2 => x2.toInt }
      val (g, d) = (is2(0), is2(1))
      List(x, (g - 30000*d)*6)
    }.filter( x => x(1) >= 3000000 )
    if( gds == List() ){ 
      println("NO")
      return
    }
    val idx = gds(0)(0)
    println("YES")
    (1 to 6).map { x =>
      println(idx)
    }
  }
}

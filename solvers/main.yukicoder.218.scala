import scala.io.StdIn.readLine
import scala.collection.immutable.StringLike
import scala.collection.immutable.Stream
import Math.{sqrt, pow}
import scala.util.control.Breaks

object Main {
  val inf2 = Stream.from(1)
  val inf3 = Stream.continually(1)
  val _lmax  = Long.MaxValue
  val _imax  = Int.MaxValue
  val b1   = new Breaks
  def main(args: Array[String]){
    val ins = (1 to 3).map { x => 
       readLine().toInt
    }
    val (a, b, c) = (ins(0), ins(1), ins(2)) 
    var ab = a/b
    if (a%b != 0 )  ab += 1 
    
    var ac = a/c
    if (a%c != 0 ) ac += 1
    if ( ac/ab.toDouble <=2/3.0 ) {
      println("YES")
    } else {
      println("NO")
    }
  }
}

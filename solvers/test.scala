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
    val a:String = new String("a")
    val b:String = new String("a")
    val c:String = "a"
    val d:String = "a"
    println( a == b )
    println( a.equalsIgnoreCase(b) )
    println( c == d )
    println( c.equalsIgnoreCase(d) )
    println( a == c )
    println( a.hashCode )
    println( c.hashCode )
  }
}

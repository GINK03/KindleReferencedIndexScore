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
    val li1 = readLine().split(" ").map{ x=> x.toInt }
    val li2:List[Int] = readLine().split(" ").map{ x=> x.toInt }.toList
    val srss = List(li1(0)*2 + li1(1)*2, li1(1)*2 + li1(2)*2, li1(2)*2+li1(0)*2)
    val combis = srss.toList.combinations(3).flatMap { _.permutations }.toList.map { x =>
      x.zip(li2).map { x => x._1 * x._2 }.reduceLeft { (a,x) => a+x }
    }.sortWith( (a,b) => a < b )
    println(combis(0))
  }
}

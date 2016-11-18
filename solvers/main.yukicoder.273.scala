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
    val s = readLine().toList
    val len = s.length
    if ( len == 2 ) {
      if(s(0) == s(1)) {
        println("1")
        return
      }else {
        println("1")
        return
      }
    }
    val res = (0 to len-1).map { x =>
      var min = 0
      if (x >= len-1-x){
        min = len-1-x
      }else{
        min = x
      }
      // println(x, min, x, len-1-x)
      // midあり
      val norder = s.slice(x+1, min+x+1)
      val mid    = s(x)
      val rorder = s.slice(x-min, x).reverse
      // midなし p1
      val norder2 = s.slice(x+1, min+x+1)
      val rorder2 = s.slice(x-min+1, x+1).reverse
      // midなし p2
      val norder3 = s.slice(x+0, min+x+0)
      val rorder3 = s.slice(x-min+0, x+0).reverse
      //println(rorder, mid, norder)
      //println(rorder2, norder2)
      val mid_num =  norder.zip(rorder).takeWhile { x => x._1 == x._2 }.length*2 + 1
      val nomid_num = norder2.zip(rorder2).takeWhile { x => x._1 == x._2 }.length*2
      val nomid2_num = norder3.zip(rorder3).takeWhile { x => x._1 == x._2 }.length*2
      List(mid_num, nomid_num, nomid2_num)
    }.flatMap { x => x}.sortWith { (a,b) => a > b }
    println(res(0))
  }
}

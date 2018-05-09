package main

import (
     "fmt"
     "net/http"
     "time"
     "io/ioutil"
     "strconv"
)

func MakeRequest(url string, ch chan<-string) {
  start := time.Now()
  var netClient = &http.Client{
    Timeout: time.Second * 60,
  }
  resp, err := netClient.Get(url)
  if err != nil {
    fmt.Printf("%s", err)
    return
  }
  defer resp.Body.Close()
  contents, err := ioutil.ReadAll(resp.Body)
  if err != nil {
      fmt.Printf("%s", err)
      return
  }
  secs := time.Since(start).Seconds()
  ch <- fmt.Sprintf("%.2f elapsed with response length: %d %s", secs, len(contents), url)
}

func main() {
  var urls []string
  for i := 1; i <= 500; i++ {
    fmt.Println(i)
    urls = append(urls, "https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid=" + strconv.Itoa(i) + "&format=json")
  }

  start := time.Now()
  ch := make(chan string)
  for _, url := range urls {
    go MakeRequest(url, ch)
  }

  for range urls {
    fmt.Println(<-ch)
  }
  fmt.Printf("%.2fs elapsed\n", time.Since(start).Seconds())
}

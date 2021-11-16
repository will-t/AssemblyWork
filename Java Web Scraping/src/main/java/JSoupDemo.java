import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

import java.io.IOException;

public class JSoupDemo {

    public static void main(String[] args) throws IOException {
        Document doc = Jsoup.connect("http://en.wikipedia.org/").get();
        System.out.println(doc.title());

        Elements newsHeadlines = doc.select("#mp-itn li");
        for (int i = 0; i < newsHeadlines.size(); i++) {
            String headline = newsHeadlines.get(i).text();
            System.out.println(headline);
        }
    }
}

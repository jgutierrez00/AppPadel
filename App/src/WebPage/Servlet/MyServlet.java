package WebPage.Servlet;
import javax.servlet.*;
import java.io.*;
import javax.servlet.http.*;

public class MyServlet extends HttpServlet{
    
    public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException{
        response.setContentType("text/html");
        PrintWriter pw = response.getWriter();
        pw.println("<!DOCTYPE html><html><head><title>Prueba</title><body><h1>Hello World!</h1></body></head></html>");
    }
}

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Prueba {

    public static void main(String[] args){
        String dni; Reservas r = new Reservas();
        BufferedReader bf = new BufferedReader(new InputStreamReader(System.in));
        Intervalo i; 
        String hora;
        while(true){
            try{
                System.out.print("Introduzca su dni: ");
                dni = bf.readLine();
                System.out.println(r.getHoras());
                System.out.println(r.toString());
                System.out.print("Introduzca hora de inicio (hh:mm): ");
                hora = bf.readLine();
                Hora h1 = new Hora(Integer.parseInt(hora.substring(0,2)), Integer.parseInt(hora.substring(3, 5)));
                if(h1.getMinutos() == 0){
                    h1 = new Hora(h1.getHora());
                }
                System.out.print("Introduzca hora de finalizacion (hh:mm): ");
                hora = bf.readLine();
                Hora h2 = new Hora(Integer.parseInt(hora.substring(0,2)), Integer.parseInt(hora.substring(3, 5)));
                if(h2.getMinutos() == 0){
                    h2 = new Hora(h2.getHora());
                }
                i = new Intervalo(h1,h2);
                r.addReserva(i, dni);
                System.out.println("Hora reservada\n");
                System.out.println(r.toString());
            }catch(AppException e){
                System.err.print(e.getMessage());
                continue;
            }catch(IOException e){
                System.err.print("Ha habido un error al guardar los datos.\n");
                continue;
            }catch(NumberFormatException e){
                System.err.print("Ha habido un error al transformar los datos.\n");
            }
            
        }
        
        
    }
    
}

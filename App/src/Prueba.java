import java.util.Scanner;

public class Prueba {

    public static void main(String[] args){
        try(Scanner sc = new Scanner(System.in)){
            String dni; Reservas r = new Reservas();
            Intervalo i; 
            String hora;
            while(true){
                System.out.print("Introduzca su dni: ");
                dni = sc.nextLine();
                System.out.println(r.getHoras());
                System.out.println(r.toString());
                System.out.print("Introduzca hora de inicio (hh:mm): ");
                hora = sc.nextLine();
                Hora h1 = new Hora(Integer.parseInt(hora.substring(0,2)), Integer.parseInt(hora.substring(3, 5)));
                if(h1.getMinutos() == 0){
                    h1 = new Hora(h1.getHora());
                }
                System.out.print("Introduzca hora de finalizacion (hh:mm): ");
                hora = sc.nextLine();
                Hora h2 = new Hora(Integer.parseInt(hora.substring(0,2)), Integer.parseInt(hora.substring(3, 5)));
                if(h2.getMinutos() == 0){
                    h2 = new Hora(h2.getHora());
                }
                i = new Intervalo(h1,h2);
                r.addReserva(i, dni);
                System.out.println("Hora reservada");
                System.out.println(r.toString());
            }
        }catch(Exception e){
            e.printStackTrace();
        }
        
    }
    
}

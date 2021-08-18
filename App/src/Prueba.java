import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Prueba {

    public static void main(String[] args){
        String s; Reservas r = new Reservas();
        BufferedReader bf = new BufferedReader(new InputStreamReader(System.in));
        Intervalo i; int ops;
        String hora;
        while(true){
            try{
                System.out.print("Operaciones: \n");
                System.out.println("(1) Añadir reserva");
                System.out.println("(2) Eliminar reserva");
                System.out.println("(3) Comprobar horas");
                System.out.println("(4) Comprobar reservas\n");
                System.out.println("Introduzca una operacion (el numero de la izquierda): ");
                s = bf.readLine();
                ops = Integer.parseInt(s);
                switch(ops){
                    case 1:
                        System.out.println("\nIntroduzca su dni: ");
                        s = bf.readLine();
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
                        r.addReserva(i, s);
                        System.out.println("Hora reservada\n");
                        System.out.println(r.toString()+"\n");
                    break;

                    case 2:
                        System.out.println("\nIntroduzca su dni: ");
                        s = bf.readLine();
                        System.out.println(r.eliminarReserva(s));
                        System.out.println(r.toString()+"\n");
                    break;

                    case 3:
                        System.out.println(r.getHoras());
                    break;

                    case 4:
                        System.out.println(r.toString());
                    break;
                }
                
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

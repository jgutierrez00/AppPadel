import java.util.Map;
import java.util.StringJoiner;
import java.util.TreeMap;
import java.util.List;
import java.util.LinkedList;

public class Reservas{
    private Map<String, Intervalo> m;
    private List<Intervalo> horas;

    /*
    *   Faltan horas. Al parecer hay juegos de hora y cuarto. Sobran media hora justo antes de las horas finales.
    */

    public Reservas(){
        m = new TreeMap<>();
        horas = new LinkedList<>();
        horas.add(new Intervalo(new Hora(10), new Hora(11,30)));
        horas.add(new Intervalo(new Hora(11,30), new Hora(13)));
        horas.add(new Intervalo(new Hora(13), new Hora(14,30)));
        horas.add(new Intervalo(new Hora(17), new Hora(18,30)));
        horas.add(new Intervalo(new Hora(18,30), new Hora(20)));
        horas.add(new Intervalo(new Hora(20), new Hora(21,30)));

    }

    public void addReserva(Intervalo i, String dni){
        checkIntervaloHora(i);
        checkIntervaloMinutos(i);
        if(checkReservaPorDni(dni)){
            throw new AppException("Usted ya ha realizado una reserva");
        }
        if(!checkHoraReservada(i)){
            throw new AppException("El intervalo de horas introducido ya ha sido reservado");
        }
        m.put(dni, i);
        horas.remove(i);

    }

    public boolean checkReservaPorDni(String dni){
        return m.get(dni) != null;
    }

    public boolean checkHoraReservada(Intervalo i){
        if(horas.contains(i)){
            return true;
        }else{
            return false;
        }
    }

    public String getHoras(){
        StringJoiner sj = new StringJoiner(", ");
        for(Intervalo i : horas){
            sj.add(i.toString());
        }
        return "Horas disponibles: "+sj.toString();
    }

    @Override
    public String toString(){
        String s = "Reservas: ";
        StringJoiner sj = new StringJoiner(",\n           ", "[", "]");

        for(String i : m.keySet()){
            sj.add(i+", "+m.get(i).toString());
        }

        return s+sj.toString();
    }

    private void checkIntervaloHora(Intervalo i){
        if(i.getHora1().getHora() < 10 || i.getHora1().getHora() > 22){
            throw new AppException("La primera hora del intervalo introducido se encuentra fuera de los intervalos establecidos");
        }else if(i.getHora2().getHora() < 10 || i.getHora2().getHora() > 22){
            throw new AppException("La segunda hora del intervalo introducido se encuentra fuera de los intervalos establecidos");
        }
    }

    private void checkIntervaloMinutos(Intervalo i){
        if(i.getHora1().getMinutos() < 0 || i.getHora1().getMinutos() > 60){
            throw new AppException("La primera hora del intervalo introducido se encuentra fuera de los intervalos establecidos");
        }else if(i.getHora2().getMinutos() < 0 || i.getHora2().getMinutos() > 60){
            throw new AppException("La segunda hora del intervalo introducido se encuentra fuera de los intervalos establecidos");
        }
    }
}
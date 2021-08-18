package AppReservas;
import java.util.Map;
import java.util.StringJoiner;
import java.util.TreeMap;
import java.util.Set;
import java.util.TreeSet;

public class Reservas{
    private Map<String, Intervalo> m;
    private Set<Intervalo> horas;

    /*
    *   Faltan horas. Al parecer hay juegos de hora y cuarto. Sobran media hora justo antes de las horas finales.
    */

    public Reservas(){
        m = new TreeMap<>();
        horas = new TreeSet<>();
        horas.add(new Intervalo(new Hora(10), new Hora(11,30)));
        horas.add(new Intervalo(new Hora(11,30), new Hora(13)));
        horas.add(new Intervalo(new Hora(13), new Hora(14,30)));
        horas.add(new Intervalo(new Hora(17), new Hora(18,30)));
        horas.add(new Intervalo(new Hora(18,30), new Hora(20)));
        horas.add(new Intervalo(new Hora(20), new Hora(21,30)));

    }

    public String addReserva(Intervalo i, String dni){
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

        return "Hora reservada con exito";
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

    public String eliminarReserva(String dni){
        if(checkReservaPorDni(dni)){
            Intervalo i = m.get(dni);
            m.remove(dni);
            horas.add(i);
            return "Hora reservada eliminada con exito";
        }
        return "Usted no ha reservado ninguna hora";

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
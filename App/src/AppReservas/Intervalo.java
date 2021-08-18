package AppReservas;
public class Intervalo implements Comparable<Intervalo>{
    private Hora h1;
    private Hora h2;

    public Intervalo(Hora h1, Hora h2){
        this.h1 = h1;
        this.h2 = h2;
    }

    public Hora getHora1(){
        return h1;
    }

    public Hora getHora2(){
        return h2;
    }

    public void setHora1(Hora h1){
        this.h1 = h1;
    }

    public void setHora2(Hora h2){
        this.h2 = h2;
    }

    @Override
    public boolean equals(Object o){
        if(o instanceof Intervalo){
            Intervalo i = (Intervalo)o;
            if(i.getHora1().equals(h1) && i.getHora2().equals(h2)){
                return true;
            }
        }
        return false;
    }

    @Override
    public int hashCode(){
        return h1.hashCode()+h2.hashCode();
    }

    @Override
    public String toString(){
        return "["+h1.toString()+","+h2.toString()+"]";
    }

    @Override
    public int compareTo(Intervalo i){
        if(h1.compareTo(i.h1) > 0){
            return 1;
        }else if(h1.compareTo(i.h1) < 0){
            return -1;
        }else{
            return 0;
        }

    }
}

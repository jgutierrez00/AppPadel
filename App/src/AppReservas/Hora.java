package AppReservas;
public class Hora implements Comparable<Hora>{

    private Integer h;
    private Integer min;

    public Hora(Integer h){
        this.h = h;
        min = 00;
    }

    public Hora(Integer h, Integer min){
        this.h = h;
        this.min = min;
    }

    public Integer getHora(){
        return h;
    }
    
    public Integer getMinutos(){
        return min;
    }

    public void setHora(Integer h){
        this.h = h;
    }

    public void setMinutos(Integer min){
        this.min = min;
    }

    @Override
    public String toString(){
        if(min == 0){
            return Integer.toString(h);
        }
        return h + ":" + min;
    }

    @Override
    public boolean equals(Object o){
        if(o instanceof Hora){
            Hora h = (Hora)o;
            if(h.h == this.h && h.min == this.min){
                return true;
            }
        }
        return false;
    }

    @Override
    public int hashCode(){
        return h.hashCode() + min.hashCode();
    }

    @Override
    public int compareTo(Hora o1) {
        if(h > o1.h){
            return 1;
        }else if(h < o1.h){
            return -1;
        }else{
            if(min > o1.min){
                return 1;
            }else if(min < o1.min){
                return -1;
            }else{
                return 0;
            }
        }
    }
}

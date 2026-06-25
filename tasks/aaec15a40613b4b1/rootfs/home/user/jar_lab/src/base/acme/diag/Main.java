package acme.diag;

public final class Main {
    private Main() {
    }

    public static void main(String[] args) {
        System.out.println("diag-probe 1.2.0: " + VersionProbe.runtime());
    }
}

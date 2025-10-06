import numpy as np
import pyvista as pv
import matplotlib.pyplot as plt

def criar_funcao_2d_terminal():
    func_str = input("Digite a função de x usando 'np', ex: np.sin(x)*x**2: ")
    try:
        x = np.linspace(-10, 10, 1000)
        y = eval(func_str, {"x": x, "np": np})
        plt.figure(figsize=(6,5))
        plt.plot(x, y)
        plt.grid(True)
        plt.title(f"y = {func_str}")
        plt.show()

        salvar = input("Deseja salvar PNG em ultra-resolução 2D? (s/n): ").lower() == 's'
        if salvar:
            x_hr = np.linspace(-10, 10, 4000)
            y_hr = eval(func_str, {"x": x_hr, "np": np})
            plt.figure(figsize=(12,12), dpi=300)
            plt.plot(x_hr, y_hr)
            plt.grid(True)
            plt.title(f"y = {func_str}")
            arquivo = input("Digite o nome do arquivo PNG: ")
            plt.savefig(arquivo, dpi=300)
            print(f"PNG salvo em ultra-resolução: {arquivo}")
    except Exception as e:
        print(f"Erro na função 2D: {e}")

def criar_funcao_3d_terminal():
    print("Digite a função ou objeto 3D.")
    print("Você pode usar:")
    print("- Função contínua Z=f(X,Y), ex: np.sin(np.sqrt(X**2+Y**2))")
    print("- Superfície paramétrica usando U e V, ex:")
    print("  X = 2*np.sin(U)*np.cos(V)")
    print("  Y = 2*np.sin(U)*np.sin(V)")
    print("  Z = 2*np.cos(U)")
    try:
        # Pergunta se é paramétrica
        tipo = input("É superfície paramétrica? (s/n): ").lower()
        if tipo == 's':
            exec_X = input("Digite X(U,V) = ")
            exec_Y = input("Digite Y(U,V) = ")
            exec_Z = input("Digite Z(U,V) = ")

            # Malha de U e V
            U = np.linspace(0, np.pi, 1000)
            V = np.linspace(0, 2*np.pi, 1000)
            U, V = np.meshgrid(U, V)

            # Avaliar as expressões
            X = eval(exec_X, {"U": U, "V": V, "np": np})
            Y = eval(exec_Y, {"U": U, "V": V, "np": np})
            Z = eval(exec_Z, {"U": U, "V": V, "np": np})

            grid = pv.StructuredGrid(X, Y, Z)
            plotter = pv.Plotter()
            plotter.add_mesh(grid, show_edges=True, color='lightblue')
            plotter.show_grid()
            plotter.add_axes()
            plotter.show()

            salvar = input("Deseja salvar PNG 3D em ultra-resolução? (s/n): ").lower() == 's'
            if salvar:
                U_hr = np.linspace(0, np.pi, 4000)
                V_hr = np.linspace(0, 2*np.pi, 4000)
                U_hr, V_hr = np.meshgrid(U_hr, V_hr)
                X_hr = eval(exec_X, {"U": U_hr, "V": V_hr, "np": np})
                Y_hr = eval(exec_Y, {"U": U_hr, "V": V_hr, "np": np})
                Z_hr = eval(exec_Z, {"U": U_hr, "V": V_hr, "np": np})
                grid_hr = pv.StructuredGrid(X_hr, Y_hr, Z_hr)
                plotter_hr = pv.Plotter(off_screen=True)
                plotter_hr.add_mesh(grid_hr, show_edges=True, color='lightblue')
                plotter_hr.show_grid()
                plotter_hr.add_axes()
                arquivo = input("Digite o nome do arquivo PNG 3D: ")
                plotter_hr.screenshot(arquivo)
                print(f"PNG 3D salvo em ultra-resolução: {arquivo}")

        else:
            func_str = input("Digite Z=f(X,Y) usando 'np', ex: np.sin(np.sqrt(X**2+Y**2)): ")
            x = np.linspace(-10, 10, 1000)
            y = np.linspace(-10, 10, 1000)
            X, Y = np.meshgrid(x, y)
            Z = eval(func_str, {"X": X, "Y": Y, "np": np})

            grid = pv.StructuredGrid(X, Y, Z)
            plotter = pv.Plotter()
            plotter.add_mesh(grid, show_edges=True, color='lightblue')
            plotter.show_grid()
            plotter.add_axes()
            plotter.show()

            salvar = input("Deseja salvar PNG 3D em ultra-resolução? (s/n): ").lower() == 's'
            if salvar:
                x_hr = np.linspace(-10, 10, 4000)
                y_hr = np.linspace(-10, 10, 4000)
                X_hr, Y_hr = np.meshgrid(x_hr, y_hr)
                Z_hr = eval(func_str, {"X": X_hr, "Y": Y_hr, "np": np})
                grid_hr = pv.StructuredGrid(X_hr, Y_hr, Z_hr)
                plotter_hr = pv.Plotter(off_screen=True)
                plotter_hr.add_mesh(grid_hr, show_edges=True, color='lightblue')
                plotter_hr.show_grid()
                plotter_hr.add_axes()
                arquivo = input("Digite o nome do arquivo PNG 3D: ")
                plotter_hr.screenshot(arquivo)
                print(f"PNG 3D salvo em ultra-resolução: {arquivo}")

    except Exception as e:
        print(f"Erro na função 3D: {e}")

# ---------------- Terminal Menu ----------------
while True:
    print("\nMenu:")
    print("1 - Criar função 2D")
    print("2 - Criar função 3D")
    print("0 - Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        criar_funcao_2d_terminal()
    elif opcao == "2":
        criar_funcao_3d_terminal()
    elif opcao == "0":
        break
    else:
        print("Opção inválida!")

import pandas as pd

folder_path = "deck/"
csv_path = folder_path + "deck.csv"
output_latex_file = "cards.tex"

def generate_latex(df, n):
    header = r'''
    \documentclass{article}
    \usepackage{graphicx}
    \usepackage[paperwidth=210mm, paperheight=297mm, margin=0cm, noheadfoot]{geometry}
    \renewcommand{\arraystretch}{1.5}  % Increase row height in tabular
    \setlength{\tabcolsep}{0pt}        % Set column separation to zero
    \pagestyle{empty}
    \begin{document}
    '''

    footer = r'''
    \end{document}
    '''

    body = ""

    for i in range(0, min(n, len(df)), 9):
        body += r'''
        \noindent
        \vspace*{\fill}
        \begin{center}
        \begin{tabular}{ccc}
        '''
        for j in range(9):
            if i + j < min(n, len(df)):
                code = df.iloc[i + j, 1]
                image_path = f"{folder_path}{code}.png"
                body += r'''
                \begin{minipage}[b]{63mm}
                \includegraphics[width=63mm, height=88mm]{%s}
                \end{minipage}
                ''' % image_path
                if (j + 1) % 3 != 0:
                    body += r'\hspace{3mm}'  # Add 5mm space between columns
                if (j + 1) % 3 == 0 and (j + 1) % 9 != 0:
                    body += r'''\\[3mm]'''  # Add 5mm space between rows
            else:
                break
        body += r'''
        \end{tabular}
        \end{center}
        \vspace*{\fill}
        '''
        if i + 9 < min(n, len(df)):
            body += r'''\newpage'''

    return header + body + footer

if __name__ == "__main__":
    try:
        n = int(input("Enter the number of images to use: "))
        if n <= 0:
            print("Please enter a positive number.")
        else:
            df = pd.read_csv(csv_path)
            latex_content = generate_latex(df, n)
            with open(output_latex_file, 'w') as f:
                f.write(latex_content)
            print(f"LaTeX file {output_latex_file} generated successfully.")
    except ValueError:
        print("Please enter a valid number.")

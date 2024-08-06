import pandas as pd

folder_path = "deck/"
csv_path = folder_path + "deck.csv"
output_latex_file = "cards.tex"

def generate_latex(df, total_count):
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
    current_count = 0

    while current_count < total_count:
        body += r'''
        \noindent
        \vspace*{\fill}
        \begin{center}
        \begin{tabular}{ccc}
        '''
        for row in range(3):
            for col in range(3):
                if current_count < total_count:
                    card_index = 0
                    while df.iloc[card_index, 2] <= 0:
                        card_index += 1
                    code = df.iloc[card_index, 1]
                    image_path = f"{folder_path}{code}.png"
                    
                    body += r'''
                    \begin{minipage}[b]{63mm}
                    \includegraphics[width=63mm, height=88mm]{%s}
                    \end{minipage}
                    ''' % image_path

                    # Update the count and the amount
                    df.at[card_index, 'Amount'] -= 1
                    current_count += 1

                    if col < 2:
                        body += r'\hspace{5mm}'  # Add 5mm space between columns
                else:
                    break
            if row < 2:
                body += r'''\\[5mm]'''  # Add 5mm space between rows
        body += r'''
        \end{tabular}
        \end{center}
        \vspace*{\fill}
        '''
        if current_count < total_count:
            body += r'''\newpage'''

    return header + body + footer

if __name__ == "__main__":
    try:
        df = pd.read_csv(csv_path)
        n = int(input("Enter the number of images to use (0 for all): "))
        if n < 0:
            print("Please enter a positive number.")
            exit(1)
        elif n == 0:
            total_count = df['Amount'].sum()
            print(f"Generating with all cards ({total_count} total)...")
        else:
            total_count = n

        latex_content = generate_latex(df, total_count)

        with open(output_latex_file, 'w') as f:
            f.write(latex_content)
        print(f"LaTeX file {output_latex_file} generated successfully.")
    except ValueError:
        print("Please enter a valid number.")
        exit(1)

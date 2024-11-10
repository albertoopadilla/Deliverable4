import csv
import os

def generate_nav_html(directory):
    base_dir = directory
    men_links = []
    women_links = []
    for subdir, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".html"):
                filepath = os.path.join(subdir, filename)
                relative_path = os.path.relpath(filepath, base_dir)
                
                if "womens_team" in subdir:
                    link = f'<a href="../womens_team/{filename}">{filename}</a>'
                    women_links.append(link)
                elif "mens_team" in subdir:
                    link = f'<a href="../mens_team/{filename}">{filename}</a>'
                    men_links.append(link)
                
    men_links_html = "\n".join(men_links)
    women_links_html = "\n".join(women_links)
    
    nav_html = f"""
    <nav>
        <ul>
            <li>
                <details>
                    <summary>Men's Team</summary>
                    <ul>
                        {men_links_html}
                    </ul>
                </details>
            </li>
            <li>
                <details>
                    <summary>Women's Team</summary>
                    <ul>
                        {women_links_html}
                    </ul>
                </details>
            </li>
        </ul>
    </nav>
    """
    
    return nav_html

def process_athlete_data(file_path):

   # Extracting athlete stats by year
   records = []

   # Extracting athlete races
   races = []           

   athlete_name = ""
   athlete_id = ""
   comments = ""

   with open(file_path, newline='', encoding='utf-8') as file:
      reader = csv.reader(file)
      data = list(reader)

      athlete_name = data[0][0]
      athlete_id = data[1][0]
      print(f"The athlete id for {athlete_name} is {athlete_id}")

      for row in data[5:-1]:
         if row[2]:
            records.append({"year": row[2], "sr": row[3]})
         else:
            races.append({
               "finish": row[1],
               "time": row[3],
               "meet": row[5],
               "url": row[6],
               "comments": row[7]
            })

   return {
      "name": athlete_name,
      "athlete_id": athlete_id,
      "season_records": records,
      "race_results": races,
      "comments": comments
   }    

def gen_athlete_page(data, outfile, nav_html):
    html_content = f'''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <link rel = "stylesheet" href = "../css/reset.css">
        <link rel = "stylesheet" href = "../css/style.css">
        <link href="../dist/css/lightbox.css" rel="stylesheet" />
        <script src="../dist/js/lightbox-plus-jquery.js"></script>
        
        <title>{data["name"]}</title>
    </head>
    <body>
      <header>
        <div>
            <a href = "../main_page/main.html">Go back to Main Menu</a>
        </div>

      {nav_html}

      
            
            <h1>{data["name"]}</h1>
            
            <a href="../images/profiles/{data["athlete_id"]}.jpg" target="_blank" data-lightbox="tea">
                <img id="athlete-image" src="../images/profiles/{data["athlete_id"]}.jpg" alt="Athlete headshot" width="200"> 
            </a>
      </header>
      <main id = "main">
         <section id= "athlete-sr-table">
               <h2><i class="fas fa-medal"></i> Athlete's Seasonal Records (SR) per Year</h2>
                <div>
                    <button id="sortByYear">Sort by Year</button>
                    <button id="sortByResult">Sort by Result</button>
                </div>
                  <table>
                        <thead>
                           <tr>
                              <th> Year </th>
                              <th> Season Record (SR)</th>
                           </tr>
                        </thead>
                        <tbody>
                    '''
      
    for sr in data["season_records"]:
        sr_row = f'''
                         <tr>
                            <td>{sr["year"]}</td>
                            <td>{sr["sr"]}</td>
                         </tr>
                   '''
        html_content += sr_row

    html_content += '''                   
                    </tbody>
                </table>
        </section>
        
        <section id="athlete-result-table">
            <h2><i class="fas fa-shoe-prints"></i> Race Results</h2>
            <div><input type="text" id="searchInput" placeholder="Search for a race..." aria-label="Use the bar to search for a race"></div>
            <div>
               <button id="sortByTime">Sort by Athlete Time</button>
               <button id="sortByPlace">Sort by Athlete Place</button>
               <button id="resetOrder">Default Order</button>
            </div>

                <table id="athlete-table">
                      <thead>
                         <tr>
                            <th><i class="fas fa-running"></i> Race</th> <!-- Running icon -->
                            <th><i class="fas fa-stopwatch"></i> Athlete Time</th> <!-- Stopwatch icon -->
                            <th><i class="fas fa-medal"></i> Athlete Place</th> <!-- Medal icon -->
                            <th><i class="fas fa-comments"></i> Race Comments</th> <!-- Comments icon -->

                         </tr>
                      </thead>

                      <tbody>
                  '''

    for race in data["race_results"]:
        race_row = f'''
                             <tr class="result-row">
                                <td>
                                   <a href="{race["url"]}">{race["meet"]}</a>
                                </td>
                                <td>{race["time"]}</td>
                                <td>{race["finish"]}</td>
                                <td>{race["comments"]}</td>
                             </tr>
        '''
        html_content += race_row

    html_content += '''
                      </tbody>
                </table>
        </section>
        
        <section id="gallery">
            <h2><i class="fas fa-images"></i> Gallery</h2>
        </section>
    </main>
    
    <footer>
        <p>
            Skyline High School<br>
            <address>
                2552 North Maple Road<br>
                Ann Arbor, MI 48103<br><br>
                <a href = "https://sites.google.com/aaps.k12.mi.us/skylinecrosscountry2021/home">XC Skyline Page</a><br>
                Follow us on Instagram <a href = "https://www.instagram.com/a2skylinexc/" aria-label="Follow Skyline High School Cross Country on Instagram"><i class="fa-brands fa-instagram" aria-label="Instagram"></i></a>
            </address>
        </p>
    </footer>
<script src="../js/js.js"></script>
</body>
</html>
'''

    with open(outfile, 'w') as output:
        output.write(html_content)

def main():
    import glob
    
    # Generate the navigation HTML
    nav_html = generate_nav_html(os.getcwd())

    # Process men's team
    folder_path = 'Deliverable3-main/mens_team'
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
    csv_file_names = [os.path.basename(file) for file in csv_files]

    print(csv_file_names)
    for file in csv_file_names:
        athlete_data = process_athlete_data("Deliverable3-main/mens_team/"+file)
        gen_athlete_page(athlete_data, "Deliverable3-main/mens_team/"+file.replace(".csv", ".html"), nav_html)

    # Process women's team
    folder_path = 'Deliverable3-main/womens_team/'
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
    csv_file_names = [os.path.basename(file) for file in csv_files]

    print(csv_file_names)
    for file in csv_file_names:
        athlete_data = process_athlete_data("Deliverable3-main/womens_team/"+file)
        gen_athlete_page(athlete_data, "Deliverable3-main/womens_team/"+file.replace(".csv", ".html"), nav_html)

if __name__ == '__main__':
    main()
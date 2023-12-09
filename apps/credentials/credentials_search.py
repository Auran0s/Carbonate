import yaml

def search_value_in_yaml(search_value):
    with open("apps/credentials/services/services.yml", "r") as f:
        services_listing = yaml.safe_load(f)

        # Parcourir la structure de données pour rechercher la valeur
        results = []
        search_recursive(services_listing, search_value.lower(), results)
        
        return list(results)

def search_recursive(data, search_value, results):
    if isinstance(data, dict):
        if 'name' in data and isinstance(data['name'], str) and search_value in data['name'].lower():
            results.append(data)
        for value in data.values():
            if isinstance(value, (dict, list)):
                search_recursive(value, search_value, results)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                search_recursive(item, search_value, results)
                
def generate_html_code(results, credentials_user_list):
    html_code = ""
    for result in results:
        name = result.get('name', '')
        img = result.get('img', '')
        desc = result.get('desc', '')
        machine = result.get('machine_name', '')

        if result['machine_name'] in [cred.name for cred in credentials_user_list]:
          html_code += f"""
          <a class="group flex flex-col justify-center bg-white border border-black-5 shadow-sm rounded-xl hover:shadow-md transition max-h-min" href="integrations/s/{machine}">
            <div class="p-4 md:p-5 space-y-4">
              <div class="flex flex-row justify-between">
                <div class="flex flex-row items-center gap-4">
                  <div class="w-8">
                    <img src="{img}" alt="">
                  </div>
                  <div>
                    <h3 class="group-hover:text-blue font-semibold text-black-100">{name}</h3>
                  </div>
                </div>
                <div>
                  <span class="inline-flex justify-center items-center gap-1.5 py-1.5 px-3 rounded-full font-inter text-xs font-semibold bg-green-light text-green-dark">
                    <svg xmlns="http://www.w3.org/2000/svg" width="8" height="8" viewBox="0 0 8 8" fill="none">
                        <path d="M4.25001 7.73294C3.21592 7.73294 2.32956 7.3693 1.59092 6.64203C0.852287 5.91476 0.488651 5.02839 0.500014 3.98294C0.488651 2.96021 0.852287 2.08521 1.59092 1.35794C2.32956 0.630665 3.21592 0.267029 4.25001 0.267029C5.25001 0.267029 6.11933 0.630665 6.85797 1.35794C7.60797 2.08521 7.98865 2.96021 8.00001 3.98294C7.98865 4.67612 7.80683 5.3068 7.45456 5.87498C7.11365 6.44317 6.65911 6.89771 6.09092 7.23862C5.53411 7.56817 4.92047 7.73294 4.25001 7.73294Z" fill="currentColor"/>
                    </svg>
                    Connected
                  </span>
                </div>
              </div>
              <div>
                <p class="font-inter font-normal text-black-50 text-xs group-hover:text-black-100">
                  {desc}
                </p>
              </div>
            </div>
          </a>
          """
        else:
          html_code += f"""
          <a class="group flex flex-col justify-center bg-white border border-black-5 shadow-sm rounded-xl hover:shadow-md transition max-h-min" href="integrations/s/{machine}">
            <div class="p-4 md:p-5 space-y-4">
              <div class="flex flex-row justify-between">
                <div class="flex flex-row items-center gap-4">
                  <div class="w-8">
                    <img src="{img}" alt="">
                  </div>
                  <div>
                    <h3 class="group-hover:text-blue font-semibold text-black-100">{name}</h3>
                  </div>
                </div>
                <div>
                  <span class="inline-flex justify-center items-center gap-1.5 py-1.5 px-3 rounded-full font-inter text-xs font-semibold bg-black-25 text-black-100">
                    <svg xmlns="http://www.w3.org/2000/svg" width="8" height="8" viewBox="0 0 8 8" fill="none">
                        <path d="M4.25001 7.73294C3.21592 7.73294 2.32956 7.3693 1.59092 6.64203C0.852287 5.91476 0.488651 5.02839 0.500014 3.98294C0.488651 2.96021 0.852287 2.08521 1.59092 1.35794C2.32956 0.630665 3.21592 0.267029 4.25001 0.267029C5.25001 0.267029 6.11933 0.630665 6.85797 1.35794C7.60797 2.08521 7.98865 2.96021 8.00001 3.98294C7.98865 4.67612 7.80683 5.3068 7.45456 5.87498C7.11365 6.44317 6.65911 6.89771 6.09092 7.23862C5.53411 7.56817 4.92047 7.73294 4.25001 7.73294Z" fill="currentColor"/>
                    </svg>
                    Not Connected
                  </span>
                </div>
              </div>
              <div>
                <p class="font-inter font-normal text-black-50 text-xs group-hover:text-black-100">
                  {desc}
                </p>
              </div>
            </div>
          </a>
          """
    return html_code
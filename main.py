from indeed.indeed_class import Indeed

with Indeed() as bot:
    bot.land_first_page()
    bot.get_rid_off_cookies_bar()
    bot.input_job_type(input("Jakiej pracy szukasz?\n"))
    bot.input_location(input("W jakim mieście?\n"))
    bot.click_search()
    bot.pull_jobs()
    bot.save_to_json()
    bot.save_to_csv()
    bot.print_as_dataframe()
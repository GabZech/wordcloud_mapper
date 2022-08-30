#%%
import wordcloud_mapper as wcm
import matplotlib.pyplot as plt

df_deu = wcm.load_companies("DEU")
df_ita = wcm.load_companies("ITA")

#%%
# GERMANY NUTS 1

map1 = wcm.wordcloud_map(df_deu,
                        nuts_codes="code",
                        words="name",
                        word_counts="employees",
                        colour_func="rank",
                        scale=5,
                        rendering_quality=1,
                        #min_font_size=0,
                        #max_font_size=30,
                        #font_step=1,
                        max_words=200,
                        relative_scaling=0.5,
                        prefer_horizontal=1,
                        #repeat=False,
                        border_scale="01M",
                        border_sharpness=100,
                        #nuts_year=2021,
                        #coord_system=3857,
                        shapefiles_path="ignore/NUTS_RG_01M_2021_3857.shp.zip"
                        )
#%%
map1.savefig("ignore/map_deu_nuts1.png")


#%%
# BERLIN

regions = ["DE3"]
df_deu = df_deu.loc[df_deu['code'].isin(regions)]

map2 = wcm.wordcloud_map(df_deu,
                        nuts_codes="code",
                        words="name",
                        word_counts="employees",
                        colour_func="random",
                        colour_hue=0,
                        scale=5,
                        rendering_quality=1,
                        #min_font_size=0,
                        #max_font_size=30,
                        #font_step=1,
                        max_words=200,
                        relative_scaling=0.5,
                        prefer_horizontal=0.9,
                        #repeat=False,
                        border_scale="01M",
                        border_sharpness=100,
                        #nuts_year=2021,
                        #coord_system=3857,
                        shapefiles_path="ignore/NUTS_RG_01M_2021_3857.shp.zip"
                        )


#%%
map2.savefig("ignore/map_DE3.png")

#%%
# NORTHERN ITALY (NUTS 2)

regions = ["ITC1", "ITC2", "ITC3", "ITC4",
           "ITH1", "ITH2", "ITH3", "ITH4", "ITH5"]
df_ita = df_ita.loc[df_ita['code'].isin(regions)]

map3 = wcm.wordcloud_map(df_ita,
                        nuts_codes="code",
                        words="name",
                        word_counts="employees",
                        colour_func="frequency",
                        scale=5,
                        rendering_quality=1,
                        #min_font_size=0,
                        #max_font_size=30,
                        #font_step=1,
                        max_words=200,
                        relative_scaling=0.5,
                        prefer_horizontal=1,
                        #repeat=False,
                        border_scale="01M",
                        border_sharpness=100,
                        #nuts_year=2021,
                        #coord_system=3857,
                        shapefiles_path="ignore/NUTS_RG_01M_2021_3857.shp.zip"
                        )
#map3.savefig("map_ita.svg")

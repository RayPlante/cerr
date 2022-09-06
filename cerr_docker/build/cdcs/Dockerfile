ARG PYTHON_VERSION
FROM python:$PYTHON_VERSION
LABEL maintainer="National Institute of Standards and Technology"

ARG CDCS_REPO
ARG BRANCH
ARG PROJECT_NAME
ARG PIP_CONF

# Directory in container for project source files
ENV DOCKYARD_SRVPROJ="/srv/curator"

# Install necessary packages
RUN apt-get update && apt-get install -y \
    netcat vim python curl git dnsutils gettext \
    libxml2-dev libxslt-dev python-dev lib32z1-dev libssl-dev \
    python3-pip libpq-dev postgresql-client xmlsec1

# Setup pip
RUN mkdir -p /root/.config/pip
COPY pip/$PIP_CONF/pip.conf /root/.config/pip

# Install uwsgi
RUN pip install uwsgi psycopg2==2.8.6

# Clone git repo
RUN git clone $CDCS_REPO $DOCKYARD_SRVPROJ
RUN cd $DOCKYARD_SRVPROJ \
    && git checkout $BRANCH

# Install requirements
WORKDIR $DOCKYARD_SRVPROJ
RUN pip install -r requirements.txt

RUN echo "\ncore-module-blob-host-app==1.21.*" >> requirements.core.txt
#RUN echo "\ngit+https://gitlab.nist.gov/gitlab/snb24/ce-registry.git@pip-package" >> requirements.core.txt

RUN pip install -r requirements.core.txt

# Copy settings file
# COPY ./settings/$BRANCH/$PROJECT_NAME.settings.py $DOCKYARD_SRVPROJ/$PROJECT_NAME/settings.py
COPY ./cerr/cerr.settings.py $DOCKYARD_SRVPROJ/$PROJECT_NAME/settings.py
COPY ./cerr/cerr.core_settings.py $DOCKYARD_SRVPROJ/$PROJECT_NAME/core_settings.py

# copy federationmetadata.xml for external SAML
COPY ./cerr/federationmetadata.xml ${DOCKYARD_SRVPROJ}/federationmetadata.xml

# workaround for SAML error in 2.16:
COPY ./cerr/attr-map.py ${DOCKYARD_SRVPROJ}/attr-maps/attr-map.py
COPY ./cerr/CERR_schema.xsd ${DOCKYARD_SRVPROJ}/static/xsd/CERR_schema.xsd
# COPY ./ghgr/list.xsl ${DOCKYARD_SRVPROJ}/static/xsl/registry-list.xsl
# COPY ./ghgr/detail.xsl ${DOCKYARD_SRVPROJ}/static/xsl/registry-detail.xsl
#COPY ./ghgr/update_xslt.py ${DOCKYARD_SRVPROJ}/update_xslt.py
COPY ./cerr/cerr-config.json ${DOCKYARD_SRVPROJ}/static/json/cerr-config.json


######### CERR CUSTOMIZATIONS ##########

#COPY ./ghgr/core_explore_keyword_app.user.index.html $DOCKYARD_SRVPROJ/templates/core_explore_keyword_app/user/index.html
#COPY $DOCKYARD_SRVPROJ/ghgr/templates/theme/index/html $DOCKYARD_SRVPROJ/templates/core_explore_keyword_app/user/index.html

COPY ./cerr/btn_custom.css ${DOCKYARD_SRVPROJ}/static/css/btn_custom.css
COPY ./cerr/extra.css ${DOCKYARD_SRVPROJ}/static/css/extra.css
COPY ./cerr/homepage.css $DOCKYARD_SRVPROJ/static/core_main_app/css/homepage.css
COPY ./cerr/main.css ${DOCKYARD_SRVPROJ}/static/css/main.css
COPY ./cerr/menu.css $DOCKYARD_SRVPROJ/static/core_main_app/css/menu.css

COPY ./cerr/banner.html $DOCKYARD_SRVPROJ/templates/theme/banner.html
COPY ./cerr/homepage.html $DOCKYARD_SRVPROJ/templates/core_main_app/user/homepage.html
COPY ./cerr/menu.html $DOCKYARD_SRVPROJ/templates/theme/menu.html
COPY ./cerr/tiles.html $DOCKYARD_SRVPROJ/templates/${PROJECT_NAME}_home/tiles.html

COPY ./cerr/views.py $DOCKYARD_SRVPROJ/${PROJECT_NAME}_home/views.py

COPY ./cerr/cerr-background.jpg ${DOCKYARD_SRVPROJ}/static/img/cerr-background.jpg
COPY ./cerr/circular.png ${DOCKYARD_SRVPROJ}/static/img/circular.png
# COPY ./ghgr/nist_logo.png ${DOCKYARD_SRVPROJ}/static/img/nist_logo.png
# COPY ./ghgr/help.html $DOCKYARD_SRVPROJ/templates/core_website_app/user/help.html
COPY ./cerr/context_processor.py $DOCKYARD_SRVPROJ/${PROJECT_NAME}_home/context_processor.py
# COPY ./ghgr/terms-of-use.html $DOCKYARD_SRVPROJ/templates/core_website_app/user/terms-of-use.html
# COPY ./ghgr/rules_of_behavior.html $DOCKYARD_SRVPROJ/templates/core_website_app/user/rules_of_behavior.html
# COPY ./ghgr/selection.css /usr/local/lib/python3.7/site-packages/core_main_registry_app/static/core_main_registry_app/user/css/resource_banner/selection.css
# COPY ./ghgr/filters.css /usr/local/lib/python3.7/site-packages/core_explore_keyword_registry_app/static/core_explore_keyword_registry_app/user/css/search/filters.css

COPY ./cerr/core_dashboard_registry_app_views.py /usr/local/lib/python3.7/site-packages/core_dashboard_registry_app/core_dashboard_registry_app/views/common/views.py

# enable core_module_blob_host_app urls and associated REST endpoints by copying
# our customized nmrr_urls into the container:
COPY ./cerr/nmrr_urls.py ${PROJECT_NAME}/urls.py

# COPY ./ghgr/favicon.ico ${DOCKYARD_SRVPROJ}/static/img/favicon.ico
# RUN sed -i 's|img/favicon.png|img/favicon.ico|g' ${DOCKYARD_SRVPROJ}/templates/theme.html

#COPY --chown=root:staff ./nestr/curate_menu_add_icon.py /usr/local/lib/python3.7/site-packages/core_curate_app/menus.py
#RUN chmod 644 /usr/local/lib/python3.7/site-packages/core_curate_app/menus.py

#COPY --chown=root:staff ./nestr/explore_menu_add_icon.py /usr/local/lib/python3.7/site-packages/core_explore_keyword_app/menus.py
#RUN chmod 644 /usr/local/lib/python3.7/site-packages/core_explore_keyword_app/menus.py

#COPY --chown=root:staff ./nestr/dashboard_menu_add_icon.py /usr/local/lib/python3.7/site-packages/core_dashboard_registry_app/menus.py
#RUN chmod 644 /usr/local/lib/python3.7/site-packages/core_dashboard_registry_app/menus.py

# disable autocomplete on login page:
RUN sed -i 's|label="Password", required=True, widget=forms.PasswordInput|label="Password", required=True, widget=forms.PasswordInput(attrs={"autocomplete": "off"})|g' /usr/local/lib/python3.7/site-packages/core_main_app/views/user/forms.py

# change link for privacy policy menu
RUN sed -i 's|reverse("core_website_app_privacy")|"https://www.nist.gov/privacy-policy"|g' /usr/local/lib/python3.7/site-packages/core_website_app/menus.py

# Change favicon of project:
RUN sed -i 's|favicon.png|circular.png|g' $DOCKYARD_SRVPROJ/templates/theme.html

# Change name of project in footer:
RUN sed -i 's|Materials Resource Registry|Circular Economy Resource Registry|g' $DOCKYARD_SRVPROJ/templates/theme/footer/default.html

#Remove open record on click=
RUN sed -i 's|$(".view-record-btn").on(|//$(".view-record-btn").on(|g' /usr/local/lib/python3.7/site-packages/core_dashboard_common_app/static/core_dashboard_common_app/common/js/list/view_record.js

#Curate with cerr app
# RUN sed -i 's|import core_curate_app.components.curate_data_structure.api as curate_data_structure_api|import core_curate_app.components.curate_data_structure.api as curate_data_structure_api\nfrom cerr_curate_app.components.curate_data_structure import api as curate_api|g' $DOCKYARD_SRVPROJ/templates/theme/footer/default.html

# remove sorting from child leaves of refinements
# RUN sed -i 's|for key, value in sorted(leaves.items()):|for key, value in leaves.items():|g' /usr/local/lib/python3.7/site-packages/core_main_registry_app/utils/refinement/refinement.py


# override pagination limit to very high value on record list page (useful
# when a record needs to be edited, since it allows a user to Ctrl-F in the
# browser in order to find the record that needs to be edited - does not affect
# the pagination limit on the query page)
#RUN sed -i 's/RECORD_PER_PAGE_PAGINATION = getattr(settings, "RESULTS_PER_PAGE", 10)/RECORD_PER_PAGE_PAGINATION = 10000/g' /usr/local/lib/python3.7/site-packages/core_dashboard_common_app/settings.py && \
#    sed -i '/RECORD_PER_PAGE_PAGINATION = 10000/a # inserted for NESTR to make workspace-list-records page show all records (or at least a large number of them) to make it easier to find a record to edit' /usr/local/lib/python3.7/site-packages/core_dashboard_common_app/settings.py



########################################

# Get entrypoint ready for the image
COPY ./docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

# Create folder for uwsgi socket
RUN mkdir /tmp/curator
# Create folder for static files
RUN mkdir $DOCKYARD_SRVPROJ/static.prod

# Create unprivileged user
RUN groupadd cdcs && \
    adduser cdcs --disabled-password --gecos '' --ingroup cdcs  && \
    chown -R cdcs:cdcs $DOCKYARD_SRVPROJ /tmp/curator

USER cdcs


ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["curator"]

Pingback
========

Pingback service serving GET requests with ``taskId`` and ``postId``

Backend Storage
---------------
* Redis


Deployments
-----------

Google AppEngine
^^^^^^^^^^^^^^^^

**On Google Could Command-Line**

.. code-block:: bash

  git clone https://github.com/Gatsby-Lee/Pingback.git
  virtualenv -p python3 ~/py3_env/Pingback
  pip install -r requirements.txt


**For AppEngine - Standard**

.. code-block:: bash

  gcloud app deploy app.standard.yaml


**For AppEngine - Flexible**

.. code-block:: bash

  gcloud app deploy app.flexible.yaml


To monitor logs

.. code-block:: bash

  gcloud app logs tail -s pingback



uWSGI stand-alone
^^^^^^^^^^^^^^^^^



Nginx + uWSGI
^^^^^^^^^^^^^


Environment Variables
---------------------

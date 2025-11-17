{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "746d3a79",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Collecting streamlit\n",
      "  Downloading streamlit-1.51.0-py3-none-any.whl.metadata (9.5 kB)\n",
      "Requirement already satisfied: altair!=5.4.0,!=5.4.1,<6,>=4.0 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from streamlit) (5.5.0)\n",
      "Collecting blinker<2,>=1.5.0 (from streamlit)\n",
      "  Downloading blinker-1.9.0-py3-none-any.whl.metadata (1.6 kB)\n",
      "Collecting cachetools<7,>=4.0 (from streamlit)\n",
      "  Downloading cachetools-6.2.2-py3-none-any.whl.metadata (5.6 kB)\n",
      "Collecting click<9,>=7.0 (from streamlit)\n",
      "  Downloading click-8.3.1-py3-none-any.whl.metadata (2.6 kB)\n",
      "Requirement already satisfied: numpy<3,>=1.23 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from streamlit) (2.3.4)\n",
      "Requirement already satisfied: packaging<26,>=20 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from streamlit) (25.0)\n",
      "Requirement already satisfied: pandas<3,>=1.4.0 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from streamlit) (2.3.3)\n",
      "Requirement already satisfied: pillow<13,>=7.1.0 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from streamlit) (11.1.0)\n",
      "Collecting protobuf<7,>=3.20 (from streamlit)\n",
      "  Downloading protobuf-6.33.1-cp310-abi3-win_amd64.whl.metadata (593 bytes)\n",
      "Requirement already satisfied: pyarrow<22,>=7.0 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from streamlit) (21.0.0)\n",
      "Requirement already satisfied: requests<3,>=2.27 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from streamlit) (2.32.5)\n",
      "Requirement already satisfied: tenacity<10,>=8.1.0 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from streamlit) (9.1.2)\n",
      "Collecting toml<2,>=0.10.1 (from streamlit)\n",
      "  Downloading toml-0.10.2-py2.py3-none-any.whl.metadata (7.1 kB)\n",
      "Requirement already satisfied: typing-extensions<5,>=4.4.0 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from streamlit) (4.15.0)\n",
      "Collecting watchdog<7,>=2.1.5 (from streamlit)\n",
      "  Downloading watchdog-6.0.0-py3-none-win_amd64.whl.metadata (44 kB)\n",
      "Collecting gitpython!=3.1.19,<4,>=3.0.7 (from streamlit)\n",
      "  Downloading gitpython-3.1.45-py3-none-any.whl.metadata (13 kB)\n",
      "Collecting pydeck<1,>=0.8.0b4 (from streamlit)\n",
      "  Downloading pydeck-0.9.1-py2.py3-none-any.whl.metadata (4.1 kB)\n",
      "Requirement already satisfied: tornado!=6.5.0,<7,>=6.0.3 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from streamlit) (6.5.1)\n",
      "Requirement already satisfied: jinja2 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (3.1.6)\n",
      "Requirement already satisfied: jsonschema>=3.0 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (4.25.1)\n",
      "Requirement already satisfied: narwhals>=1.14.2 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (2.10.1)\n",
      "Requirement already satisfied: colorama in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from click<9,>=7.0->streamlit) (0.4.6)\n",
      "Collecting gitdb<5,>=4.0.1 (from gitpython!=3.1.19,<4,>=3.0.7->streamlit)\n",
      "  Downloading gitdb-4.0.12-py3-none-any.whl.metadata (1.2 kB)\n",
      "Collecting smmap<6,>=3.0.1 (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit)\n",
      "  Downloading smmap-5.0.2-py3-none-any.whl.metadata (4.3 kB)\n",
      "Requirement already satisfied: python-dateutil>=2.8.2 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from pandas<3,>=1.4.0->streamlit) (2.9.0.post0)\n",
      "Requirement already satisfied: pytz>=2020.1 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from pandas<3,>=1.4.0->streamlit) (2025.2)\n",
      "Requirement already satisfied: tzdata>=2022.7 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from pandas<3,>=1.4.0->streamlit) (2025.2)\n",
      "Requirement already satisfied: charset_normalizer<4,>=2 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from requests<3,>=2.27->streamlit) (3.4.4)\n",
      "Requirement already satisfied: idna<4,>=2.5 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from requests<3,>=2.27->streamlit) (3.11)\n",
      "Requirement already satisfied: urllib3<3,>=1.21.1 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from requests<3,>=2.27->streamlit) (2.5.0)\n",
      "Requirement already satisfied: certifi>=2017.4.17 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from requests<3,>=2.27->streamlit) (2025.10.5)\n",
      "Requirement already satisfied: MarkupSafe>=2.0 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from jinja2->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (3.0.3)\n",
      "Requirement already satisfied: attrs>=22.2.0 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (25.4.0)\n",
      "Requirement already satisfied: jsonschema-specifications>=2023.03.6 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (2025.9.1)\n",
      "Requirement already satisfied: referencing>=0.28.4 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (0.37.0)\n",
      "Requirement already satisfied: rpds-py>=0.7.1 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (0.28.0)\n",
      "Requirement already satisfied: six>=1.5 in c:\\users\\godyuniron\\anaconda3\\envs\\examenv\\lib\\site-packages (from python-dateutil>=2.8.2->pandas<3,>=1.4.0->streamlit) (1.17.0)\n",
      "Downloading streamlit-1.51.0-py3-none-any.whl (10.2 MB)\n",
      "   ---------------------------------------- 0.0/10.2 MB ? eta -:--:--\n",
      "   ------------- -------------------------- 3.4/10.2 MB 18.3 MB/s eta 0:00:01\n",
      "   ----------------------------- ---------- 7.6/10.2 MB 19.6 MB/s eta 0:00:01\n",
      "   ---------------------------------------- 10.2/10.2 MB 18.6 MB/s  0:00:00\n",
      "Downloading blinker-1.9.0-py3-none-any.whl (8.5 kB)\n",
      "Downloading cachetools-6.2.2-py3-none-any.whl (11 kB)\n",
      "Downloading click-8.3.1-py3-none-any.whl (108 kB)\n",
      "Downloading gitpython-3.1.45-py3-none-any.whl (208 kB)\n",
      "Downloading gitdb-4.0.12-py3-none-any.whl (62 kB)\n",
      "Downloading protobuf-6.33.1-cp310-abi3-win_amd64.whl (436 kB)\n",
      "Downloading pydeck-0.9.1-py2.py3-none-any.whl (6.9 MB)\n",
      "   ---------------------------------------- 0.0/6.9 MB ? eta -:--:--\n",
      "   ------------------ --------------------- 3.1/6.9 MB 16.8 MB/s eta 0:00:01\n",
      "   --------------------------------- ------ 5.8/6.9 MB 13.6 MB/s eta 0:00:01\n",
      "   ---------------------------------------- 6.9/6.9 MB 13.3 MB/s  0:00:00\n",
      "Downloading smmap-5.0.2-py3-none-any.whl (24 kB)\n",
      "Downloading toml-0.10.2-py2.py3-none-any.whl (16 kB)\n",
      "Downloading watchdog-6.0.0-py3-none-win_amd64.whl (79 kB)\n",
      "Installing collected packages: watchdog, toml, smmap, protobuf, click, cachetools, blinker, pydeck, gitdb, gitpython, streamlit\n",
      "\n",
      "   ----------------------------------------  0/11 [watchdog]\n",
      "   ---------- -----------------------------  3/11 [protobuf]\n",
      "   ---------- -----------------------------  3/11 [protobuf]\n",
      "   ---------- -----------------------------  3/11 [protobuf]\n",
      "   -------------- -------------------------  4/11 [click]\n",
      "   --------------------- ------------------  6/11 [blinker]\n",
      "  Attempting uninstall: pydeck\n",
      "   --------------------- ------------------  6/11 [blinker]\n",
      "    Found existing installation: pydeck 0.2.1\n",
      "   --------------------- ------------------  6/11 [blinker]\n",
      "    Uninstalling pydeck-0.2.1:\n",
      "   --------------------- ------------------  6/11 [blinker]\n",
      "      Successfully uninstalled pydeck-0.2.1\n",
      "   --------------------- ------------------  6/11 [blinker]\n",
      "   ------------------------- --------------  7/11 [pydeck]\n",
      "   ------------------------- --------------  7/11 [pydeck]\n",
      "   ------------------------- --------------  7/11 [pydeck]\n",
      "   ----------------------------- ----------  8/11 [gitdb]\n",
      "   -------------------------------- -------  9/11 [gitpython]\n",
      "   -------------------------------- -------  9/11 [gitpython]\n",
      "   ------------------------------------ --- 10/11 [streamlit]\n",
      "   ------------------------------------ --- 10/11 [streamlit]\n",
      "   ------------------------------------ --- 10/11 [streamlit]\n",
      "   ------------------------------------ --- 10/11 [streamlit]\n",
      "   ------------------------------------ --- 10/11 [streamlit]\n",
      "   ------------------------------------ --- 10/11 [streamlit]\n",
      "   ------------------------------------ --- 10/11 [streamlit]\n",
      "   ------------------------------------ --- 10/11 [streamlit]\n",
      "   ------------------------------------ --- 10/11 [streamlit]\n",
      "   ------------------------------------ --- 10/11 [streamlit]\n",
      "   ------------------------------------ --- 10/11 [streamlit]\n",
      "   ------------------------------------ --- 10/11 [streamlit]\n",
      "   ------------------------------------ --- 10/11 [streamlit]\n",
      "   ------------------------------------ --- 10/11 [streamlit]\n",
      "   ------------------------------------ --- 10/11 [streamlit]\n",
      "   ---------------------------------------- 11/11 [streamlit]\n",
      "\n",
      "Successfully installed blinker-1.9.0 cachetools-6.2.2 click-8.3.1 gitdb-4.0.12 gitpython-3.1.45 protobuf-6.33.1 pydeck-0.9.1 smmap-5.0.2 streamlit-1.51.0 toml-0.10.2 watchdog-6.0.0\n"
     ]
    }
   ],
   "source": [
    "!pip install streamlit"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "9dca0a97",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import altair as alt"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "ebad13e0",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-11-17 13:58:34.602 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-11-17 13:58:34.603 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-11-17 13:58:34.605 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "DeltaGenerator()"
      ]
     },
     "execution_count": 2,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import streamlit as st\n",
    "\n",
    "#타이틀 텍스트 출력\n",
    "st.title('이것은 나의 첫번째 Streamlit 웹 어플')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "28f4ddbf",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-11-17 14:00:10.176 No runtime found, using MemoryCacheStorageManager\n",
      "2025-11-17 14:00:10.183 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-11-17 14:00:10.184 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-11-17 14:00:10.185 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-11-17 14:00:10.188 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-11-17 14:00:10.189 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-11-17 14:00:10.190 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-11-17 14:00:10.192 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-11-17 14:00:10.193 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-11-17 14:00:10.194 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-11-17 14:00:10.207 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-11-17 14:00:10.208 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-11-17 14:00:10.209 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-11-17 14:00:10.294 Please replace `use_container_width` with `width`.\n",
      "\n",
      "`use_container_width` will be removed after 2025-12-31.\n",
      "\n",
      "For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'` or specify an integer width.\n",
      "2025-11-17 14:00:10.295 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-11-17 14:00:10.296 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-11-17 14:00:10.298 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    }
   ],
   "source": [
    "@st.cache_data\n",
    "def get_un_data() -> pd.DataFrame:\n",
    "    aws_bucket_url = \"https://streamlit-demo-data.s3-us-west-2.amazonaws.com\"\n",
    "    df = pd.read_csv(aws_bucket_url + \"/agri.csv.gz\")\n",
    "    return df.set_index(\"Region\")\n",
    "\n",
    "try:\n",
    "    df = get_un_data()\n",
    "    countries = st.multiselect(\n",
    "        \"Choose countries\", list(df.index), [\"China\", \"United States of America\"]\n",
    "    )\n",
    "    if not countries:\n",
    "        st.error(\"Please select at least one country.\")\n",
    "    else:\n",
    "        data = df.loc[countries]\n",
    "        data /= 1000000.0\n",
    "        st.subheader(\"Gross agricultural production ($B)\")\n",
    "        st.dataframe(data.sort_index())\n",
    "\n",
    "        data = data.T.reset_index()\n",
    "        data = pd.melt(data, id_vars=[\"index\"]).rename(\n",
    "            columns={\"index\": \"year\", \"value\": \"Gross Agricultural Product ($B)\"}\n",
    "        )\n",
    "        chart = (\n",
    "            alt.Chart(data)\n",
    "            .mark_area(opacity=0.3)\n",
    "            .encode(\n",
    "                x=\"year:T\",\n",
    "                y=alt.Y(\"Gross Agricultural Product ($B):Q\", stack=None),\n",
    "                color=\"Region:N\",\n",
    "            )\n",
    "        )\n",
    "        st.altair_chart(chart, use_container_width=True)\n",
    "except URLError as e:\n",
    "    st.error(f\"This demo requires internet access. Connection error: {e.reason}\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "examenv",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.14"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

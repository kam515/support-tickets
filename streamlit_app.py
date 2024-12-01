import datetime
import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import supabase
from supabase import create_client, Client
import streamlit.components.v1 as components


# Show app title and description.
st.set_page_config(page_title="Support tickets", page_icon="🎫")
st.title("🎫 Support tickets")
st.write(
    """
    This app shows how you can build an internal tool in Streamlit. Here, we are 
    implementing a support ticket workflow. The user can create a ticket, edit 
    existing tickets, and view some statistics.
    """
)

st.markdown('| 1 | 2 | 3 |\n|---|---|---|\n|   |   |   |\n|   |   |   |')

# CUSTOM COMPONENT FOR MERMAID RENDERING!!!
# def mermaid(code: str) -> None:
#     components.html(
#         f"""
#         <pre class="mermaid">
#             {code}
#         </pre>

#         <script type="module">
#             import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
#             mermaid.initialize({{ startOnLoad: true }});
#         </script>
#         """
#     )
def mermaid(code: str, height: int = 100) -> None:
    """
    Renders a Mermaid diagram using Streamlit's HTML components with adjustable height.

    Args:
        code (str): The Mermaid diagram definition as a string.
        height (int): The height of the rendered component in pixels.
    """
    components.html(
        f"""
        <pre class="mermaid">
            {code}
        </pre>

        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
        """,
        height=height,  # Set the height dynamically
        scrolling=False  # Allow scrolling for larger diagrams
    )

def mermaid_no_h(code: str) -> None:
    """
    Renders a Mermaid diagram using Streamlit's HTML components with adjustable height.

    Args:
        code (str): The Mermaid diagram definition as a string.
        height (int): The height of the rendered component in pixels.
    """
    components.html(
        f"""
        <pre class="mermaid">
            {code}
        </pre>

        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
        """
    )

def mermaid_dynamic(code: str) -> None:
    """
    Renders a Mermaid diagram in Streamlit with dynamic height adjustment.

    Args:
        code (str): The Mermaid diagram definition as a string.
    """
    components.html(
        f"""
        <div id="mermaid-container">
            <pre class="mermaid">
                {code}
            </pre>
        </div>

        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
            
            // Adjust height dynamically after rendering
            const observer = new ResizeObserver(() => {{
                const container = document.getElementById('mermaid-container');
                if (container) {{
                    const contentHeight = container.scrollHeight;
                    window.parent.postMessage({{ height: contentHeight }}, '*');
                }}
            }});
            observer.observe(document.getElementById('mermaid-container'));
        </script>
        """,
        height=100,  # Initial height for loading; will adjust dynamically
        scrolling=False  # Disable scrolling; height adjusts to content
    )

def mermaid_dynamic_2(code: str) -> None:
    """
    Renders a Mermaid diagram using Streamlit's HTML components with dynamic height.

    Args:
        code (str): The Mermaid diagram definition as a string.
    """
    components.html(
        f"""
        <div id="mermaid-container">
            <pre class="mermaid">{code}</pre>
        </div>

        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});

            // Function to dynamically adjust height
            window.addEventListener('load', () => {{
                const container = document.getElementById('mermaid-container');
                const height = container.scrollHeight;
                container.style.height = height + 'px'; // Set height dynamically
            }});
        </script>
        """,
        height=500,  # Initial height (adjusted later)
        scrolling=False  # No scrolling needed since height will adapt
    )

def mermaid_with_div(code: str, height: int = 100) -> None:
    """
    Renders a Mermaid diagram using Streamlit's HTML components with adjustable height.

    Args:
        code (str): The Mermaid diagram definition as a string.
        height (int): The height of the rendered component in pixels.
    """
    components.html(
        f"""
        <div style="height:{height}px; overflow: auto;">
            <pre class="mermaid">
                {code}
            </pre>
        </div>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
        """,
        height=height,  # Set the height dynamically for the component
        scrolling=True  # Allow scrolling for larger diagrams
    )

mermaid_no_h(
    """
    graph LR
        A --> B --> C
    """
)





name = "km123"

url: str = st.secrets.get("SUPABASE_URL")
key: str = st.secrets.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Function to fetch data with caching
@st.cache_data
def fetch_data():
    response = supabase.table("my_first_table").select("*").execute()
    if response.data:
        return pd.DataFrame(response.data)
    return pd.DataFrame()  # Return empty DataFrame if no data

# Function to insert new data
def insert_data(name):
    supabase.table("my_first_table").insert({"data": "hieiiierl", "name": name}).execute()

# Main Streamlit app logic
st.title("Welcome to My App")

# Fetch and display data
df = fetch_data()
st.dataframe(df)

# Input for the name
name = st.text_input("Enter your name:")

if name:
    if name in df["name"].values:
        st.write(f"Welcome back, {name}!")
    else:
        insert_data(name)
        st.write(f"Thanks for signing up, {name}!")

        # Update cached data to reflect the new insertion
        st.cache_data.clear()  # Clear cache to refresh the table
        df = fetch_data()
        st.dataframe(df)



mermaid_no_h("""
graph TD
    subgraph Initiation
        A1[Identify Requirements] --> A2[Feasibility Study]
        A2 --> A3[Stakeholder Approval]
    end
    
    subgraph Planning
        B1[Define Scope] --> B2[Develop Schedule]
        B2 --> B3[Resource Allocation]
        B3 --> B4[Risk Assessment]
        B4 --> B5[Finalize Plan]
    end
    
    subgraph Execution
        C1[Team Onboarding] --> C2[Task Assignments]
        C2 --> C3[Implement Deliverables]
        C3 --> C4[Quality Assurance]
    end
    
    subgraph Monitoring
        D1[Track Progress] --> D2[Report Performance]
        D2 --> D3[Manage Risks]
        D3 --> D4[Update Stakeholders]
    end
    
    subgraph Closing
        E1[Final Deliverable Review] --> E2[Stakeholder Acceptance]
        E2 --> E3[Project Retrospective]
        E3 --> E4[Archive Documents]
    end

    A3 --> B1
    B5 --> C1
    C4 --> D1
    D4 --> E1
""")




# response = supabase.table("my_first_table").select("*").execute()
# # convert to df
# response = pd.DataFrame(response.data)
# # display as a table in streamlit
# st.dataframe(response)


# if name in response["name"]:
#     st.write(f"Welcome back, {name}!")
# else:
#     response = (
#         supabase.table("my_first_table")
#         .insert({"data": "hieiiierl", "name": name})
#         .execute()
#     )
#     st.write(f"Thanks for signing up, {name}!")




# OLD CODE:

# # Create a random Pandas dataframe with existing tickets.
# if "df" not in st.session_state:

#     # Set seed for reproducibility.
#     np.random.seed(42)

#     # Make up some fake issue descriptions.
#     issue_descriptions = [
#         "Network connectivity issues in the office",
#         "Software application crashing on startup",
#         "Printer not responding to print commands",
#         "Email server downtime",
#         "Data backup failure",
#         "Login authentication problems",
#         "Website performance degradation",
#         "Security vulnerability identified",
#         "Hardware malfunction in the server room",
#         "Employee unable to access shared files",
#         "Database connection failure",
#         "Mobile application not syncing data",
#         "VoIP phone system issues",
#         "VPN connection problems for remote employees",
#         "System updates causing compatibility issues",
#         "File server running out of storage space",
#         "Intrusion detection system alerts",
#         "Inventory management system errors",
#         "Customer data not loading in CRM",
#         "Collaboration tool not sending notifications",
#     ]

    # # Generate the dataframe with 100 rows/tickets.
    # data = {
    #     "ID": [f"TICKET-{i}" for i in range(1100, 1000, -1)],
    #     "Issue": np.random.choice(['issue_descriptions'], size=100),
    #     "Status": np.random.choice(["Open", "In Progress", "Closed"], size=100),
    #     "Priority": np.random.choice(["High", "Medium", "Low"], size=100),
    #     "Date Submitted": [
    #         datetime.date(2023, 6, 1) + datetime.timedelta(days=random.randint(0, 182))
    #         for _ in range(100)
    #     ],
    # }
    # df = pd.DataFrame(data)

    # # Save the dataframe in session state (a dictionary-like object that persists across
    # # page runs). This ensures our data is persisted when the app updates.
    # st.session_state.df = df


# # Show a section to add a new ticket.
# st.header("Add a ticket")

# # We're adding tickets via an `st.form` and some input widgets. If widgets are used
# # in a form, the app will only rerun once the submit button is pressed.
# with st.form("add_ticket_form"):
#     issue = st.text_area("Describe the issue")
#     priority = st.selectbox("Priority", ["High", "Medium", "Low"])
#     submitted = st.form_submit_button("Submit")

# if submitted:
#     # Make a dataframe for the new ticket and append it to the dataframe in session
#     # state.
#     recent_ticket_number = int(max(st.session_state.df.ID).split("-")[1])
#     today = datetime.datetime.now().strftime("%m-%d-%Y")
#     df_new = pd.DataFrame(
#         [
#             {
#                 "ID": f"TICKET-{recent_ticket_number+1}",
#                 "Issue": issue,
#                 "Status": "Open",
#                 "Priority": priority,
#                 "Date Submitted": today,
#             }
#         ]
#     )

#     # Show a little success message.
#     st.write("Ticket submitted! Here are the ticket details:")
#     st.dataframe(df_new, use_container_width=True, hide_index=True)
#     st.session_state.df = pd.concat([df_new, st.session_state.df], axis=0)

# # Show section to view and edit existing tickets in a table.
# st.header("Existing tickets")
# st.write(f"Number of tickets: `{len(st.session_state.df)}`")

# st.info(
#     "You can edit the tickets by double clicking on a cell. Note how the plots below "
#     "update automatically! You can also sort the table by clicking on the column headers.",
#     icon="✍️",
# )

# # Show the tickets dataframe with `st.data_editor`. This lets the user edit the table
# # cells. The edited data is returned as a new dataframe.
# edited_df = st.data_editor(
#     st.session_state.df,
#     use_container_width=True,
#     hide_index=True,
#     column_config={
#         "Status": st.column_config.SelectboxColumn(
#             "Status",
#             help="Ticket status",
#             options=["Open", "In Progress", "Closed"],
#             required=True,
#         ),
#         "Priority": st.column_config.SelectboxColumn(
#             "Priority",
#             help="Priority",
#             options=["High", "Medium", "Low"],
#             required=True,
#         ),
#     },
#     # Disable editing the ID and Date Submitted columns.
#     disabled=["ID", "Date Submitted"],
# )

# # Show some metrics and charts about the ticket.
# st.header("Statistics")

# # Show metrics side by side using `st.columns` and `st.metric`.
# col1, col2, col3 = st.columns(3)
# num_open_tickets = len(st.session_state.df[st.session_state.df.Status == "Open"])
# col1.metric(label="Number of open tickets", value=num_open_tickets, delta=10)
# col2.metric(label="First response time (hours)", value=5.2, delta=-1.5)
# col3.metric(label="Average resolution time (hours)", value=16, delta=2)

# # Show two Altair charts using `st.altair_chart`.
# st.write("")
# st.write("##### Ticket status per month")
# status_plot = (
#     alt.Chart(edited_df)
#     .mark_bar()
#     .encode(
#         x="month(Date Submitted):O",
#         y="count():Q",
#         xOffset="Status:N",
#         color="Status:N",
#     )
#     .configure_legend(
#         orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
#     )
# )
# st.altair_chart(status_plot, use_container_width=True, theme="streamlit")

# st.write("##### Current ticket priorities")
# priority_plot = (
#     alt.Chart(edited_df)
#     .mark_arc()
#     .encode(theta="count():Q", color="Priority:N")
#     .properties(height=300)
#     .configure_legend(
#         orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
#     )
# )
# st.altair_chart(priority_plot, use_container_width=True, theme="streamlit")

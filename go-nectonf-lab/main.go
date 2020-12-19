package main

import (
	"encoding/xml"
	"flag"
	"fmt"
	"log"
	"strings"

	"github.com/Juniper/go-netconf/netconf"
	"golang.org/x/crypto/ssh"
)

func main() {
	target := flag.String("target", "localhost", "target")
	port := flag.String("port", "2830", "port")
	chassisCmd := flag.Bool("chassis", false, "get chassis serial number from 'show chassis hardware'")
	ifCmd := flag.Bool("if", false, "get if admin from 'show interface terse'")

	flag.Parse()
	c, err := NewConn(*target, *port)
	if err != nil {
		log.Fatalln(err)
	}
	defer c.conn.Close()

	if *chassisCmd {
		if err := c.GetChassisSN(); err != nil {
			log.Fatal(err)
		}
	}
	if *ifCmd {
		if err := c.GetIfAdmin(); err != nil {
			log.Fatal(err)
		}
	}
}

// Conn netconf.Session
type Conn struct {
	conn *netconf.Session
}

// NewConn Entrypoint of netconf.Session
func NewConn(target, port string) (Conn, error) {
	conf := &ssh.ClientConfig{
		User:            "root",
		Auth:            []ssh.AuthMethod{ssh.Password("Juniper")},
		HostKeyCallback: ssh.InsecureIgnoreHostKey(),
	}
	d := fmt.Sprintf("%v:%v", target, port)
	s, err := netconf.DialSSH(d, conf)
	if err != nil {
		return Conn{}, err
	}
	return Conn{conn: s}, nil
}

// GetIfAdmin get interface admin list from "show interface terse"
func (c *Conn) GetIfAdmin() error {
	out, err := c.conn.Exec(netconf.RawMethod("<get-interface-information><terse/></get-interface-information>"))
	if err != nil {
		return err
	}
	var ift InterfaceInformation
	if err = xml.Unmarshal([]byte(out.Data), &ift); err != nil {
		return err
	}
	for _, v := range ift.PhysicalInterface {
		ifName := strings.ReplaceAll(v.Name, "\n", "")
		if strings.HasPrefix(ifName, "ge") {
			adminStatus := strings.ReplaceAll(v.AdminStatus, "\n", "")
			fmt.Printf("%v : %v\n", ifName, adminStatus)
		}
	}
	return nil
}

// GetChassisSN get chassis serial number from "show chassis hardware"
func (c *Conn) GetChassisSN() error {
	out, err := c.conn.Exec(netconf.RawMethod("<get-chassis-inventory/>"))
	if err != nil {
		return err
	}
	var ci ChassisInventory
	if err = xml.Unmarshal([]byte(out.Data), &ci); err != nil {
		return err
	}

	chassisName := strings.ReplaceAll(ci.Chassis.Name, "\n", "")
	chassisSN := strings.ReplaceAll(ci.Chassis.SerialNumber, "\n", "")
	fmt.Printf("%v : %v\n", chassisName, chassisSN)

	return nil
}

// InterfaceInformation struct for "show interface terse"
type InterfaceInformation struct {
	XMLName           xml.Name `xml:"interface-information"`
	Text              string   `xml:",chardata"`
	Xmlns             string   `xml:"xmlns,attr"`
	Style             string   `xml:"style,attr"`
	PhysicalInterface []struct {
		Text             string `xml:",chardata"`
		Name             string `xml:"name"`
		AdminStatus      string `xml:"admin-status"`
		OperStatus       string `xml:"oper-status"`
		LogicalInterface []struct {
			Text              string `xml:",chardata"`
			Name              string `xml:"name"`
			AdminStatus       string `xml:"admin-status"`
			OperStatus        string `xml:"oper-status"`
			FilterInformation string `xml:"filter-information"`
			AddressFamily     []struct {
				Text              string `xml:",chardata"`
				AddressFamilyName string `xml:"address-family-name"`
				InterfaceAddress  []struct {
					Text     string `xml:",chardata"`
					IfaLocal struct {
						Text string `xml:",chardata"`
						Emit string `xml:"emit,attr"`
					} `xml:"ifa-local"`
					IfaDestination struct {
						Text string `xml:",chardata"`
						Emit string `xml:"emit,attr"`
					} `xml:"ifa-destination"`
				} `xml:"interface-address"`
			} `xml:"address-family"`
		} `xml:"logical-interface"`
	} `xml:"physical-interface"`
}

// ChassisInventory struct for "show chassis hardware"
type ChassisInventory struct {
	XMLName xml.Name `xml:"chassis-inventory"`
	Text    string   `xml:",chardata"`
	Xmlns   string   `xml:"xmlns,attr"`
	Chassis struct {
		Text          string `xml:",chardata"`
		Style         string `xml:"style,attr"`
		Name          string `xml:"name"`
		SerialNumber  string `xml:"serial-number"`
		Description   string `xml:"description"`
		ChassisModule []struct {
			Text             string `xml:",chardata"`
			Name             string `xml:"name"`
			Description      string `xml:"description"`
			ChassisSubModule struct {
				Text        string `xml:",chardata"`
				Name        string `xml:"name"`
				Description string `xml:"description"`
			} `xml:"chassis-sub-module"`
		} `xml:"chassis-module"`
	} `xml:"chassis"`
}

package main

import (
	"database/sql"
	"encoding/base64"
	"fmt"
	"time"

	"github.com/ProtonMail/go-appdir"
	"github.com/gen2brain/beeep"
	_ "github.com/lib/pq"
	"gopkg.in/ini.v1"

	"github.com/luisnquin/vert-cli/src/tasker/interfaces"
)

func main() {
	// Yes, I don't know about logs

	dir := appdir.New("vert")
	config, err := ini.Load(dir.UserConfig() + "/config.ini")
	if err != nil {
		panic(err)
	}
	encoded_dsn := config.Section("database").Key("dsn").String()
	decoded_dsn, err := base64.StdEncoding.DecodeString(encoded_dsn)
	if err != nil {
		panic(err)
	}
	conn, err := sql.Open("postgres", string(decoded_dsn))
	if err != nil {
		panic(err)
	}
	ns := interfaces.Notifications{}
	rows, err := conn.Query("SELECT * FROM notifications;")
	if err != nil {
		panic(err)
	}
	for rows.Next() {
		n := &interfaces.Notifier{}
		err = rows.Scan(&n.Id, &n.Title, &n.Message, &n.Hour)
		if err != nil {
			panic(err)
		}
		ns = append(ns, *n)
	}
	for {
		time.Sleep(time.Minute)
		current := time.Now()
		current_minute := fmt.Sprintf("%v:%v:00", current.Hour(), current.Minute())

		for _, n := range ns {
			if fmt.Sprintf("%v:%v:00", n.Hour.Hour(), n.Hour.Minute()) == current_minute {
				err := beeep.Notify(n.Title, n.Message, "/usr/sbin/vert/command-line.png")
				if err != nil {
					panic(err)
				}
			}
		}
	}
}

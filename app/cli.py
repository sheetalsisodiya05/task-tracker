"""Terminal interface.

Usage:
    python -m app.cli add "Learn Git" --priority high --due 2026-11-05
    python -m app.cli list
    python -m app.cli list --status todo
    python -m app.cli update 1 --status done
    python -m app.cli delete 1
"""
import argparse
import sys

from app import storage, utils


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tasktracker",
                                     description="Simple task manager")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a task")
    p_add.add_argument("title")
    p_add.add_argument("--priority", default="medium",
                       choices=utils.VALID_PRIORITIES)
    p_add.add_argument("--due", help="Due date, YYYY-MM-DD")

    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument("--status", choices=utils.VALID_STATUSES)

    p_upd = sub.add_parser("update", help="Update a task")
    p_upd.add_argument("id", type=int)
    p_upd.add_argument("--title")
    p_upd.add_argument("--priority", choices=utils.VALID_PRIORITIES)
    p_upd.add_argument("--status", choices=utils.VALID_STATUSES)
    p_upd.add_argument("--due")

    p_del = sub.add_parser("delete", help="Delete a task")
    p_del.add_argument("id", type=int)
    return parser


def print_tasks(tasks) -> None:
    if not tasks:
        print("No tasks found.")
        return
    print(f"{'ID':<4}{'TITLE':<30}{'PRIORITY':<10}{'STATUS':<13}DUE")
    print("-" * 66)
    for t in tasks:
        print(f"{t.id:<4}{t.title[:28]:<30}{t.priority:<10}"
              f"{t.status:<13}{t.due_date or '-'}")


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "add":
            task = storage.add_task(args.title, args.priority, args.due)
            print(f"Added task #{task.id}: {task.title}")
        elif args.command == "list":
            print_tasks(storage.list_tasks(args.status))
        elif args.command == "update":
            task = storage.update_task(args.id, title=args.title,
                                       priority=args.priority,
                                       status=args.status, due_date=args.due)
            print(f"Updated task #{task.id}")
        elif args.command == "delete":
            storage.delete_task(args.id)
            print(f"Deleted task #{args.id}")
    except storage.TaskNotFound as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except (ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

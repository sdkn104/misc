#!/usr/bin/env python3
"""
read_mail.py

Usage:
  python read_mail.py "entryid1,entryid2,..."

Given a comma-separated EntryIDCollection, fetch each mail item from Outlook
and print: Subject, To, CC, Body, Internet-Message-ID.

Note: Requires pywin32 (win32com).
"""
import sys
import traceback

try:
    import win32com.client
except Exception:
    print("Error: this script requires pywin32 (win32com). Install with: pip install pywin32")
    raise


MAPI_PR_INTERNET_MESSAGE_ID = "http://schemas.microsoft.com/mapi/proptag/0x1035001F"
MAPI_PR_SMTP_ADDRESS = "http://schemas.microsoft.com/mapi/proptag/0x39FE001E"


def get_mail_by_entryid(namespace, entry_id):
    """Try to get a MailItem by EntryID. If direct lookup fails, try each store."""
    try:
        return namespace.GetItemFromID(entry_id)
    except Exception:
        # Try each store as fallback
        for store in namespace.Stores:
            try:
                return namespace.GetItemFromID(entry_id, store.StoreID)
            except Exception:
                continue
    return None


def get_internet_message_id(mail):
    try:
        pa = mail.PropertyAccessor
        return pa.GetProperty(MAPI_PR_INTERNET_MESSAGE_ID)
    except Exception:
        return None


def get_smtp_from_addressentry(addr_entry):
    """Return an SMTP (internet) address for an AddressEntry if possible."""
    if not addr_entry:
        return None
    try:
        pa = addr_entry.PropertyAccessor
        try:
            smtp = pa.GetProperty(MAPI_PR_SMTP_ADDRESS)
            if smtp:
                return smtp
        except Exception:
            pass

        # Try Exchange user object
        try:
            exch = addr_entry.GetExchangeUser()
            if exch:
                smtp = exch.PrimarySmtpAddress
                if smtp:
                    return smtp
        except Exception:
            pass

        # Last resort: return the Address field
        try:
            return addr_entry.Address
        except Exception:
            return None
    except Exception:
        return None


def get_sender_smtp(mail):
    # Prefer Sender AddressEntry when available
    try:
        sender = getattr(mail, "Sender", None)
        if sender:
            smtp = get_smtp_from_addressentry(sender)
            if smtp:
                return smtp
    except Exception:
        pass

    # Try PropertyAccessor for PR_SMTP_ADDRESS on the message itself
    try:
        pa = mail.PropertyAccessor
        smtp = pa.GetProperty(MAPI_PR_SMTP_ADDRESS)
        if smtp:
            return smtp
    except Exception:
        pass

    # Fallback to SenderEmailAddress (may be in EX format)
    try:
        return getattr(mail, "SenderEmailAddress", None)
    except Exception:
        return None


def format_recipients(mail):
    # Build To/CC from Recipients using SMTP addresses when possible
    to_list = []
    cc_list = []
    try:
        for r in mail.Recipients:
            try:
                rtype = int(r.Type)
            except Exception:
                rtype = 0
            smtp = None
            try:
                ae = getattr(r, "AddressEntry", None)
                if ae:
                    smtp = get_smtp_from_addressentry(ae)
            except Exception:
                smtp = None

            if not smtp:
                # fallback to the simple Address property
                try:
                    smtp = getattr(r, "Address", None)
                except Exception:
                    smtp = None

            if rtype == 1 and smtp:
                to_list.append(smtp)
            elif rtype == 2 and smtp:
                cc_list.append(smtp)

    except Exception:
        pass

    # If lists are empty, fall back to To/CC strings
    to = ", ".join(to_list) if to_list else (getattr(mail, "To", "") or "")
    cc = ", ".join(cc_list) if cc_list else (getattr(mail, "CC", "") or "")

    return to, cc


def get_folder_name_for_mail(mail):
    """Return the immediate folder name containing the mail (not full path)."""
    try:
        folder = getattr(mail, "Parent", None)
        if not folder:
            return ""
        # Folder object should have a Name property
        try:
            name = getattr(folder, "Name", None)
            if name:
                return name
        except Exception:
            pass
        return ""
    except Exception:
        return ""


def print_mail(entry_id, mail):
    print("=" * 80)
    print(f"EntryID: {entry_id}")
    if mail is None:
        print("  [Not found or cannot access item]")
        return

    # Folder name
    try:
        folder_name = get_folder_name_for_mail(mail)
        if folder_name:
            print(f"Folder: {folder_name}")
    except Exception:
        pass

    subj = getattr(mail, "Subject", "")
    sender = get_sender_smtp(mail)
    to, cc = format_recipients(mail)
    body = getattr(mail, "Body", None)
    if body is None:
        # try HTML body as fallback
        body = getattr(mail, "HTMLBody", "")

    imid = get_internet_message_id(mail) or ""

    # Sent date
    sent_on = None
    try:
        sent_on = getattr(mail, "SentOn", None)
    except Exception:
        sent_on = None
    if sent_on:
        try:
            sent_on_str = sent_on.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            sent_on_str = str(sent_on)
    else:
        sent_on_str = ""

    print(f"Subject: {subj}")
    print(f"From: {sender or ''}")
    print(f"To: {to}")
    print(f"CC: {cc}")
    print(f"Internet-Message-ID: {imid}")
    print(f"SentOn: {sent_on_str}")
    print("--- Body start ---")
    # Print full body; if very large, user can redirect output
    print(body)
    print("--- Body end ---")


def main():
    if len(sys.argv) < 2:
        print("Usage: python read_mail.py \"entryid1,entryid2,...\"")
        sys.exit(1)

    entry_collection = sys.argv[1]
    if not entry_collection:
        print("No EntryIDCollection provided.")
        sys.exit(1)

    entry_ids = [e.strip() for e in entry_collection.split(",") if e.strip()]
    if not entry_ids:
        print("No valid EntryIDs parsed.")
        sys.exit(1)

    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")
    except Exception as e:
        print("Failed to connect to Outlook:", e)
        traceback.print_exc()
        sys.exit(1)

    for eid in entry_ids:
        try:
            mail = get_mail_by_entryid(namespace, eid)
            print_mail(eid, mail)
        except Exception as e:
            print("Error handling EntryID:", eid)
            traceback.print_exc()


if __name__ == "__main__":
    main()

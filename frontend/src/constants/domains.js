import {
  Laptop,
  Users,
  Scale,
  HeartPulse,
} from "lucide-react";

export const domains = [
  {
    id: "it",
    name: "IT Helpdesk",
    description: "Passwords, VPN, Outlook, Devices",
    icon: Laptop,
  },
  {
    id: "hr",
    name: "HR Policy",
    description: "Leave, Attendance, Benefits",
    icon: Users,
  },
  {
    id: "legal",
    name: "Legal & Compliance",
    description: "Contracts, NDA, Policies",
    icon: Scale,
  },
  {
    id: "healthcare",
    name: "Healthcare",
    description: "Insurance, Claims, Medical Leave",
    icon: HeartPulse,
  },
];
import { Moon, Sun, Info } from "lucide-react";
import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { useAuthStore } from "@/stores/auth.store";
import { useThemeStore } from "@/stores/theme.store";
import { useAssistantStore } from "@/stores/assistant.store";
import { initials } from "@/utils/format";

export default function SettingsPage() {
  const { fullName, email, role } = useAuthStore();
  const { theme, setTheme } = useThemeStore();
  const { streamingMode, setStreamingMode } = useAssistantStore();

  return (
    <div>
      <PageHeader title="Settings" description="Manage your profile, appearance, and workspace preferences." />

      <Tabs defaultValue="profile">
        <TabsList>
          <TabsTrigger value="profile">Profile</TabsTrigger>
          <TabsTrigger value="appearance">Appearance</TabsTrigger>
          <TabsTrigger value="assistant">Assistant</TabsTrigger>
          <TabsTrigger value="workspace">Workspace</TabsTrigger>
        </TabsList>

        <TabsContent value="profile">
          <Card>
            <CardHeader>
              <CardTitle>Your profile</CardTitle>
              <CardDescription className="mt-1">Details associated with your account.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-5">
              <div className="flex items-center gap-3">
                <Avatar className="h-14 w-14">
                  <AvatarFallback className="text-base">{initials(fullName ?? "SO")}</AvatarFallback>
                </Avatar>
                <div>
                  <p className="font-medium text-foreground">{fullName ?? "—"}</p>
                  <Badge variant="secondary" className="mt-1">
                    {role ?? "—"}
                  </Badge>
                </div>
              </div>
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <div className="space-y-1.5">
                  <Label>Full name</Label>
                  <Input value={fullName ?? ""} disabled />
                </div>
                <div className="space-y-1.5">
                  <Label>Email</Label>
                  <Input value={email ?? ""} disabled />
                </div>
              </div>
              <p className="flex items-start gap-2 text-xs text-muted-foreground">
                <Info className="mt-0.5 h-3.5 w-3.5 shrink-0" />
                Profile editing isn't available yet — the backend doesn't currently expose an endpoint to update
                user details. TODO: backend.
              </p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="appearance">
          <Card>
            <CardHeader>
              <CardTitle>Appearance</CardTitle>
              <CardDescription className="mt-1">Choose how SynapseOS looks on your device.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between rounded-lg border border-border p-4">
                <div className="flex items-center gap-3">
                  {theme === "light" ? <Sun className="h-4 w-4 text-muted-foreground" /> : <Moon className="h-4 w-4 text-muted-foreground" />}
                  <div>
                    <p className="text-sm font-medium text-foreground">Dark mode</p>
                    <p className="text-xs text-muted-foreground">Switch between light and dark themes.</p>
                  </div>
                </div>
                <Switch checked={theme === "dark"} onCheckedChange={(v) => setTheme(v ? "dark" : "light")} />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="assistant">
          <Card>
            <CardHeader>
              <CardTitle>AI Assistant</CardTitle>
              <CardDescription className="mt-1">Default behavior for the AI Assistant.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between rounded-lg border border-border p-4">
                <div>
                  <p className="text-sm font-medium text-foreground">Streaming responses</p>
                  <p className="text-xs text-muted-foreground">
                    Show the assistant's agent execution timeline live as it responds.
                  </p>
                </div>
                <Switch checked={streamingMode} onCheckedChange={setStreamingMode} />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="workspace">
          <Card>
            <CardHeader>
              <CardTitle>Workspace</CardTitle>
              <CardDescription className="mt-1">Tenant-level configuration.</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="flex items-start gap-2 text-xs text-muted-foreground">
                <Info className="mt-0.5 h-3.5 w-3.5 shrink-0" />
                Workspace/tenant settings aren't available yet — the backend exposes tenant creation only, with
                no endpoint to read or update an existing tenant's profile. TODO: backend.
              </p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
